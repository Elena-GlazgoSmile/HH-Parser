import asyncio
from app.services.nats_client import nats_client

async def test_publish():
    print("Тест публикации в NATS...")
    
    await nats_client.connect()
    
    # Tестовое сообщение
    await nats_client.publish(
        "vacancies.updates",
        {
            "type": "test_message",
            "message": "Это тест из Python скрипта",
            "test": True
        }
    )
    
    print("Сообщение опубликовано")

if __name__ == "__main__":
    asyncio.run(test_publish())