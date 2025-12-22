#!/bin/bash
echo "=== ПОЛНАЯ ПРОВЕРКА ПРОЕКТА ==="
echo ""

echo "1. 📡 Проверка здоровья сервера:"
curl -s http://localhost:8000/health | python3 -m json.tool
echo ""

echo "2. 🏠 Главная страница:"
curl -s http://localhost:8000/
echo ""
echo ""

echo "3. 📊 База данных (вакансии):"
curl -s http://localhost:8000/api/vacancies | python3 -c "
import sys, json
data = json.load(sys.stdin)
count = len(data)
print(f'   📁 Найдено вакансий: {count}')
if count > 0:
    print(f'   📝 Последние 3:')
    for i, v in enumerate(data[:3]):
        print(f'      {i+1}. {v.get(\"name\", \"Без названия\")[:40]}...')
"
echo ""
echo ""

echo "4. ⚙️ Проверка WebSocket (быстрая):"
echo "   Для полной проверки WebSocket используйте браузер (F12 → Console)"
echo "   или запустите: python test_ws_simple.py"
echo ""

echo "5. 🚀 Запуск фоновой задачи (парсинг):"
read -p "   Запустить фоновую задачу? (y/n): " choice
if [ "$choice" = "y" ]; then
    curl -X POST http://localhost:8000/api/tasks/run
    echo ""
    echo "   ✅ Задача запущена! Проверьте вакансии через 10 секунд:"
    echo "   curl http://localhost:8000/api/vacancies"
fi
