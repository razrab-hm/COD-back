import hashlib
import sys

import app.app.db as core_db
from app.models.db import auth, companies, hashrates, users


def create():
    username = input('username: ')
    password = input('password: ')
    db = core_db.get_core_db()
    user = users.User(username=username, hash_password=hashlib.md5(password.encode('utf-8')).hexdigest(), role='root', inactive=False)
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user


name = sys.argv[1]

f = globals().get(name)
if f:
    f()
