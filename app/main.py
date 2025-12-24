from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from contextlib import asynccontextmanager
import asyncio
from app.api.endpoints import router as api_router
from app.websocket.ws_manager import manager
from app.tasks.background import background_task
from app.services.nats_client import nats_client
from app.database import init_db
from app.config import settings
from datetime import datetime

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Инициализация приложения...")
    
    await init_db()
    
    await nats_client.connect()
    
    task = asyncio.create_task(background_task.start_periodic())
    
    yield
    
    print("Остановка приложения...")
    task.cancel()
    await nats_client.close()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan
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
        "database": "connected",
        "nats": "connected" if nats_client.connected else "disconnected"
    }
