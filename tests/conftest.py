import pytest

from app.models.db import users, companies, auth, hashrates
from tests.setupdb_tests import db


@pytest.fixture(autouse=True)
def clear_db():
    db.query(users.User).delete()
    db.query(users.UserCompany).delete()
    db.query(companies.Company).delete()
    db.query(hashrates.Hashrate).delete()
