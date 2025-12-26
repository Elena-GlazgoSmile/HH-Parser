import json
import nats
from app.config import settings
from datetime import datetime

class NatsClient:
    def __init__(self):
        self.nc = None
        self.connected = False
        self.message_handler = None
    
    async def connect(self):
        try:
            self.nc = await nats.connect(settings.NATS_URL)
            self.connected = True
            print("Подключен к NATS")
            
            if self.message_handler:
                await self.nc.subscribe(settings.NATS_SUBJECT, cb=self.message_handler)
                print(f"   Подписан на: {settings.NATS_SUBJECT}")
                
        except Exception as e:
            print(f"Ошибка подключения к NATS: {e}")
    
    async def publish(self, subject: str, message: dict):
        if not self.connected or not self.nc:
            print("NATS не подключен")
            return
        
        try:
            message['published_at'] = datetime.utcnow().isoformat()
            await self.nc.publish(subject, json.dumps(message).encode())
            print(f"Опубликовано в NATS [{subject}]: {message.get('type', 'unknown')}")
        except Exception as e:
            print(f"Ошибка публикации в NATS: {e}")
    
    async def close(self):
        if self.nc:
            await self.nc.close()
            self.connected = False
            print("Соединение с NATS закрыто")

nats_client = NatsClient()