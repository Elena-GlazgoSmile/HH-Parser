import json
import nats
from nats.errors import ConnectionClosedError, TimeoutError
from app.config import settings
from datetime import datetime

class NatsClient:
    def __init__(self):
        self.nc = None
        self.connected = False
    
    async def connect(self):
        try:
            self.nc = await nats.connect(settings.NATS_URL)
            self.connected = True
            print("Подключен к NATS")
            
            await self.subscribe()
            
        except Exception as e:
            print(f"Ошибка подключения к NATS: {e}")
    
    async def subscribe(self):
        if self.connected and self.nc:
            async def message_handler(msg):
                subject = msg.subject
                data = msg.data.decode()
                print(f"Получено сообщение из NATS [{subject}]: {data}")
            
            await self.nc.subscribe(settings.NATS_SUBJECT, cb=message_handler)
    
    async def publish(self, subject: str, message: dict):
        if not self.connected or not self.nc:
            print("NATS не подключен")
            return
        
        try:
            message['published_at'] = datetime.utcnow().isoformat()
            await self.nc.publish(
                subject,
                json.dumps(message).encode()
            )
            print(f"Опубликовано в NATS [{subject}]")
        except Exception as e:
            print(f"Ошибка публикации в NATS: {e}")
    
    async def close(self):
        if self.nc:
            await self.nc.close()
            self.connected = False

nats_client = NatsClient()
