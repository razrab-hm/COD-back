from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from core.db import Base


class Company(Base):
    __tablename__ = 'company'

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(30), unique=True)
    contact_name = Column(String(30))
    contact_email = Column(String(30))
    hash = relationship('Hash')
    user = relationship('User')

