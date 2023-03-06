import os

import pytest

# Edit link here and in docker compose
os.environ['DATABASE_LINK'] = 'postgresql://root:123123@127.0.0.1:5431/db01'

os.system('alembic revision --autogenerate')
os.system('alembic upgrade head')

from app.models.db import users, companies, auth, hashrates
from app.app import db as core_db

from app.tests.test_user import client

#
@pytest.fixture(autouse=True)
def clear_db():
    db = core_db.get_core_db()
    db.query(users.UserCompany).delete()
    db.query(hashrates.Hashrate).delete()
    db.query(users.User).delete()
    db.query(companies.Company).delete()
    db.commit()
    db.close()


def auth_user(db_user):
    response = client.post('/api/users/login', json={'username': db_user.username, 'password': 'qwerty'})
    return {'Authorization': f"Bearer {response.json()['access_token']}"}

