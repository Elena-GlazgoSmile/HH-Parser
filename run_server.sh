#!/bin/bash
cd /mnt/c/Users/712/hh-parser
source venv/bin/activate

echo "Запуск сервера на порту 8000..."
echo "Логи будут выводиться здесь"
echo "Для проверки откройте новый терминал (Ctrl+Shift+`)"
echo ""
echo "Проверочные команды для нового терминала:"
echo "1. curl http://localhost:8000/health"
echo "2. python -c \"import asyncio; import websockets; async def t(): async with websockets.connect('ws://localhost:8000/ws/vacancies') as w: print(await w.recv()); asyncio.run(t())\""
echo ""
echo "Для остановки сервера нажмите Ctrl+C"
echo ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
