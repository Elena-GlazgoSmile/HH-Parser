import json
from datetime import datetime
from app.websocket.ws_manager import manager
from app.services.nats_client import nats_client

class NATSWebSocketBridge:
    async def start(self):
        nats_client.message_handler = self.handle_nats_message
        if nats_client.connected:
            await nats_client.nc.subscribe("vacancies.*", cb=self.handle_nats_message)
    
    async def stop(self):
        pass
    
    async def handle_nats_message(self, msg):
        try:
            subject = msg.subject
            data = json.loads(msg.data.decode())
            
            await manager.broadcast({
                "type": "nats_message",
                "subject": subject,
                "data": data,
                "timestamp": datetime.utcnow().isoformat()
            })
            
            print(f"NATS → WebSocket: {subject}")
            
        except Exception as e:
            print(f"Ошибка в мосте: {e}")

bridge = NATSWebSocketBridge()