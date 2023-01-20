from core.db import Base, SessionLocal
from services.users import models
from services.companies import models
from services.permissions import models
from services.hashs import models


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

