#!/bin/bash

echo "🚀 Быстрый запуск проекта HH Parser..."

cd /mnt/c/Users/712/hh-parser

if [ ! -d "venv" ]; then
    echo "Виртуальное окружение не найдено"
    exit 1
fi

source venv/bin/activate

if ! python -c "import fastapi" &>/dev/null; then
    echo "Зависимости не установлены. Устанавливаем..."
    pip install -r requirements.txt
fi

echo "Запускаем FastAPI сервер на порту 8000..."
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 > server.log 2>&1 &
SERVER_PID=$!
echo "PID сервера: $SERVER_PID"

sleep 3

if curl -s http://localhost:8000/health > /dev/null; then
    echo "Сервер запущен успешно!"
    echo "Документация: http://localhost:8000/docs"
    echo "WebSocket: ws://localhost:8000/ws/vacancies"
    echo "Логи сервера: tail -f server.log"
    
    echo -e "\nТестируем WebSocket..."
    cat > test_ws.html << 'HTML'
<!DOCTYPE html>
<html>
<body>
    <h2>WebSocket тест</h2>
    <button onclick="connect()">Подключиться</button>
    <button onclick="sendTest()">Отправить тест</button>
    <div id="output"></div>
    <script>
        let ws;
        function connect() {
            ws = new WebSocket('ws://localhost:8000/ws/vacancies');
            ws.onopen = () => log('Подключено');
            ws.onmessage = (e) => log(': ' + e.data);
            ws.onerror = (e) => log('Ошибка: ' + e);
            ws.onclose = () => log('Отключено');
        }
        function sendTest() {
            if (ws) ws.send('Тестовое сообщение');
        }
        function log(msg) {
            document.getElementById('output').innerHTML += msg + '<br>';
        }
    </script>
</body>
</html>
HTML
    
    echo "Откройте в браузере файл test_ws.html для тестирования WebSocket"
else
    echo "Ошибка запуска сервера. Проверьте логи:"
    tail -n 20 server.log
    kill $SERVER_PID 2>/dev/null
fi

echo -e "\nДля остановки сервера: kill $SERVER_PID"
