# COD-back
 
<h3>Запуск проекта:</h3>
- copy .env.example to .env
- set database link in alembic ini
- pip install -r requirements.txt
- docker compose up -d
- alembic revision --autogenerate
- alembic upgrade head
- uvicorn app.main:app

<h3>Создание супер-пользователя:</h3>
- python superuser.py create

