from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
from app.api.endpoints import router as api_router
from app.websocket.ws_manager import manager
from app.tasks.background import background_task
from app.services.nats_client import nats_client
from app.services.nats_to_websocket import bridge
from app.database import init_db
from app.config import settings
from datetime import datetime

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"Инициализация приложения {settings.PROJECT_NAME} v{settings.VERSION}...")
    print(f"Режим отладки: {'ВКЛ' if settings.DEBUG else 'ВЫКЛ'}")
    
    await init_db()
    await nats_client.connect()
    await bridge.start()
    
    if settings.BACKGROUND_TASK_INTERVAL > 0:
        task = asyncio.create_task(background_task.start_periodic())
    else:
        task = None
    
    yield
    
    print("Остановка приложения...")
    if task:
        task.cancel()
    await bridge.stop()
    await nats_client.close()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
    debug=settings.DEBUG
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_PREFIX)

@app.websocket("/ws/vacancies")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        await websocket.send_json({
            "type": "connection_established",
            "message": "Подключено к WebSocket вакансий",
            "timestamp": datetime.utcnow().isoformat()
        })
        
        while True:
            data = await websocket.receive_text()
            await websocket.send_json({
                "type": "echo",
                "received": data,
                "timestamp": datetime.utcnow().isoformat()
            })
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "debug": settings.DEBUG,
        "database": "connected",
        "nats": "connected" if nats_client.connected else "disconnected"
    }

@app.get("/config")
async def show_config():
    if not settings.DEBUG:
        return {"message": "Not available in production"}
    
    return {
        "project_name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "debug": settings.DEBUG,
        "database_url": settings.DATABASE_URL[:50] + "..." if len(settings.DATABASE_URL) > 50 else settings.DATABASE_URL,
        "has_redis": bool(settings.REDIS_URL),
        "has_s3": bool(settings.S3_ENDPOINT_URL and settings.S3_ACCESS_KEY),
        "workers": settings.WORKERS,
        "log_level": settings.LOG_LEVEL
    }