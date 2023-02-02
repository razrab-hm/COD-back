import hashlib
import os

os.environ['DATABASE_LINK'] = 'postgresql://root:123123@127.0.0.1:5431/db01'
os.system('alembic revision --autogenerate')
os.system('alembic upgrade head')

from app.app import db as core_db
from app.models.db import users

os.environ['DATABASE_LINK'] = 'postgresql://root:123123@127.0.0.1:5432/db01'

db = core_db.get_core_db()
user = users.User(username='root_test', hash_password=hashlib.md5('qwerty'.encode('utf-8')).hexdigest(), role='root', inactive=False)
db.add(user)
user = users.User(username='admin_test', hash_password=hashlib.md5('qwerty'.encode('utf-8')).hexdigest(), role='admin', inactive=False)
db.add(user)
user = users.User(username='manager_test', hash_password=hashlib.md5('qwerty'.encode('utf-8')).hexdigest(), role='manager', inactive=False)
db.add(user)
db.commit()
db.refresh(user)
db.close()
