# HH-Parser
Инструкция по запуску моего веб-сервера HH-Parser:
0. Установить Docker Desktop, Visual Studio Code, WSL
1. Создать папку, куда помещен будет весь проект и перейти в неё cd HH-Rarser
2. Клонирование моего репозитория из Гитхаб на компьютер https://github.com/Elena-GlazgoSmile/HH-Parser.git
3. Создать в папке проекта виртуальное окружение для работы в WSL: python -m venv venv
4. Активировать виртуальное окружение source venv/bin/activate
5. Установка зависимостей из файла requirements.txt командой в wsl: pip install -r requirements.txt
6. Запуск NATS из Docker-контейнера: docker run -p 4222:4222 -p 8222:8222 nats:latest
7. Проверка работы NATS: curl http://localhost:8222
8. В терминале, отдельном от того, где был запущен Docker-контейнер с NATS, запуск веб-сервера: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
9. Проверка работы веб-сервера: curl http://localhost:8000/health
10. (но пропустить все 5-8 пункты) Запустить NATS и веб-сервер с помощью Docker-compose: docker-compose up -d
11. Проверить запущенные контейнеры: docker-compose ps
12. Открыть веб-сервер в браузере: http://localhost:8000/docs
13. Открыть NATS в браузере: http://localhost:8222/