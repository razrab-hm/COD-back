from sqlalchemy import Column, Integer, String, ForeignKey, Boolean

from db.core_db import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, unique=True)
    email = Column(String(50))
    hash_password = Column(String(50))
    role = Column(String)
    company_id = Column(Integer, ForeignKey('company.id'))
    inactive = Column(Boolean)
