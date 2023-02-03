import os

import pytest

os.environ['DATABASE_LINK'] = 'postgresql://root:123123@127.0.0.1:5431/db01'
os.system('alembic revision --autogenerate')
os.system('alembic upgrade head')

from app.models.db import users, companies, auth, hashrates
from app.app import db as core_db


@pytest.fixture(autouse=True)
def clear_db():
    db = core_db.get_core_db()
    db.query(users.User).delete()
    db.query(users.UserCompany).delete()
    db.query(companies.Company).delete()
    db.query(hashrates.Hashrate).delete()
    db.commit()
    db.close()


# @pytest.fixture
# def
