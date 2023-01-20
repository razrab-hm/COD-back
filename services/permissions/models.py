from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from core.db import Base


class Permission(Base):
    __tablename__ = 'permission'

    id = Column(Integer, primary_key=True, unique=True)
    permission_name = Column(String(50))
    user = relationship('User')

