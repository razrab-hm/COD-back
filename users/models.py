from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import Column, String, Integer

from core.db import Base


class User(Base, SQLAlchemyBaseUserTable):
    name = Column(String, unique=True)
    id_role = Column(Integer)
    password = Column(String)
    id_company = Column(Integer)
