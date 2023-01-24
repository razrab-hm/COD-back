from sqlalchemy import Column, Integer, ForeignKey, Date, Float

from app.db import Base


class Hashrate(Base):
    __tablename__ = 'hashrate'

    id = Column(Integer, primary_key=True, unique=True)
    date = Column(Date)
    average = Column(Float)
    hash = Column(Float)
    company_id = Column(Integer, ForeignKey('company.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
