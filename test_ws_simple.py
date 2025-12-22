import asyncio
import websockets
import json

async def test():
    try:
        print("Подключаюсь к ws://localhost:8000/ws/vacancies...")
        async with websockets.connect('ws://localhost:8000/ws/vacancies') as ws:
            print("Подключено!")
            
            greeting = await ws.recv()
            data = json.loads(greeting)
            print(f"Сервер: {data['message']}")
            
            await ws.send("Тест из Python")
            response = await ws.recv()
            echo_data = json.loads(response)
            print(f"🔁 Эхо: {echo_data['received']}")
            
            print("\nWebSocket работает корректно!")
            print("Для получения уведомлений о вакансиях:")
            print("curl -X POST http://localhost:8000/api/tasks/run")
            
    except ConnectionRefusedError:
        print("Не удалось подключиться. Сервер запущен?")
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(test())
