import hashlib
import sys

from sqlalchemy.orm import Session

import app.db as core_db
from models.db import auth, companies, hashrates, users


def create():
    username = input('username: ')
    password = input('password: ')
    db = core_db.get_core_db()
    user = users.User(email=username, hash_password=hashlib.md5(password.encode('utf-8')).hexdigest(), role='root', inactive=False)
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user


name = sys.argv[1]

f = globals().get(name)
if f:
    f()
