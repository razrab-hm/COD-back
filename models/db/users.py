from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship

from app.db import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, unique=True)
    email = Column(String(50))
    hash_password = Column(Text)
    role = Column(String)
    inactive = Column(Boolean)
    company = relationship('UserCompany')
    hashrate = relationship('Hashrate')


class UserCompany(Base):
    __tablename__ = 'user_company'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    company_id = Column(Integer, ForeignKey('company.id'))

