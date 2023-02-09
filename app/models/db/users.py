from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship

from app.app.db import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, unique=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    hash_password = Column(Text, nullable=False)
    role = Column(String(10))
    description = Column(String(50))
    inactive = Column(Boolean)
    company = relationship('UserCompany')
    hashrate = relationship('Hashrate')


class UserCompany(Base):
    __tablename__ = 'user_company'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    company_id = Column(Integer, ForeignKey('company.id'))

