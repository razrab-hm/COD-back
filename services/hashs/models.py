from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import relationship

from core.db import Base


class Hash(Base):
    __tablename__ = 'hash'

    id = Column(Integer, primary_key=True, unique=True)
    date = Column(Date)
    average = Column(Float)
    hash = Column(Float)
    company_id = Column(Integer, ForeignKey('company.id'))
