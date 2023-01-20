from sqlalchemy import Column, Integer, String, ForeignKey

from db.core_db import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, unique=True)
    email = Column(String(50))
    hash_password = Column(String(50))
    permission_id = Column(Integer, ForeignKey('permission.id'))
    company_id = Column(Integer, ForeignKey('company.id'))
