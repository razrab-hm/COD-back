from sqlalchemy import Column, Integer, ForeignKey, Date, Float, String

from app.app.db import Base


class Hashrate(Base):
    __tablename__ = 'hashrate'

    id = Column(Integer, primary_key=True, unique=True)
    date = Column(Date)
    average = Column(Float)
    hash = Column(Float)
    total_profit = Column(Float)
    company_id = Column(Integer, ForeignKey('company.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
