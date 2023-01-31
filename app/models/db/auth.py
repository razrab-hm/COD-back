from sqlalchemy import Column, Integer, String

from app.app.db import Base


class Token(Base):
    __tablename__ = 'token'

    id = Column(Integer, primary_key=True, unique=True)
    refresh_token = Column(String)


