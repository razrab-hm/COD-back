# COD-back
 
<h3>Запуск проекта:</h3>
- pip install -r requirements.txt
- alembic revision --autogenerate
- alembic upgrade head
- uvicorn main:app

<h3>Создание супер-пользователя:</h3>
- python superuser.py create

