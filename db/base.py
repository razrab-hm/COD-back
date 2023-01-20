from db.core_db import SessionLocal, Base
from db.models import companies, hashrates, users


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

