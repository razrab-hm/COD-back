import hashlib
import os

import pytest

os.environ['DATABASE_LINK'] = 'postgresql://root:123123@127.0.0.1:5431/db01'
os.system('alembic revision --autogenerate')
os.system('alembic upgrade head')

from app.models.db import users, companies, auth, hashrates
from app.app import db as core_db
from app.tests.test_user import client


@pytest.fixture(autouse=True)
def clear_db():
    db = core_db.get_core_db()
    db.query(users.User).delete()
    db.query(users.UserCompany).delete()
    db.query(companies.Company).delete()
    db.query(hashrates.Hashrate).delete()
    db.commit()
    db.close()


def user():
    db = core_db.get_core_db()

    db_user = users.User(username='user',
                         email='user@mail.ru',
                         hash_password=hashlib.md5('qwerty'.encode('utf-8')).hexdigest(),
                         role='manager', inactive=False)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db.close()
    return db_user


def root_user():
    db = core_db.get_core_db()

    db_user = users.User(username='root_user',
                         email='root_user@mail.ru',
                         hash_password=hashlib.md5('qwerty'.encode('utf-8')).hexdigest(),
                         role='root', inactive=False)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db.close()
    return db_user


def admin_user():
    db = core_db.get_core_db()

    db_user = users.User(username='admin_user',
                         email='admin_user@mail.ru',
                         hash_password=hashlib.md5('qwerty'.encode('utf-8')).hexdigest(),
                         role='admin', inactive=False)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db.close()
    return db_user


def inactive_user():
    db = core_db.get_core_db()

    db_user = users.User(username='inactive_user',
                         email='inactive_user@mail.ru',
                         hash_password=hashlib.md5('qwerty'.encode('utf-8')).hexdigest(),
                         role='manager', inactive=True)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db.close()
    return db_user


def auth_user(user):
    response = client.get('/users/login', json={'username': user.username, 'password': 'qwerty'})
    return {'Authorization': f"Bearer {response['access_token']}"}

