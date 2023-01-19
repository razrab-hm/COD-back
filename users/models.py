from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from core.db import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, unique=True)
    email = Column(String(50))
    hash_password = Column(String(50))
    permission_id = Column(Integer, ForeignKey('permission.id'))


class Permission(Base):
    __tablename__ = 'permission'

    id = Column(Integer, primary_key=True, unique=True)
    permission_name = Column(String(50))
    user = relationship('User')



