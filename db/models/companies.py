from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy.orm import relationship

from db.core_db import Base


class Company(Base):
    __tablename__ = 'company'

    id = Column(Integer, primary_key=True, unique=True)
    title = Column(String(30), unique=True)
    contact_fio = Column(String(30))
    contact_email = Column(String(30))
    contact_phone = Column(String(15))
    img_logo = Column(Text)
    description = Column(Text)
    inactive = Column(Boolean)
    hash = relationship('Hashrate')
    user = relationship('UserCompany')
