import asyncio
import nats
import json

async def test_nats():
    try:
        # Подключаемся
        nc = await nats.connect("nats://localhost:4222")
        print("NATS подключен!")
        
        # Подписываемся
        async def handler(msg):
            data = json.loads(msg.data.decode())
            print(f"NATS сообщение: {data['type'] if 'type' in data else 'unknown'}")
        
        sub = await nc.subscribe("vacancies.updates", cb=handler)
        print("Подписка на vacancies.updates")
        
        await asyncio.sleep(30)
        await nc.close()
        
    except Exception as e:
        print(f"Ошибка: {e}")

asyncio.run(test_nats())
