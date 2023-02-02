import hashlib

from app.app import db as core_db
from app.models.db import users


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
