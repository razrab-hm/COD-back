import string

from fastapi import HTTPException
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship, validates

from app.app.db import Base


symbols = list(string.ascii_lowercase) + list('0123456789_-.')
email_symobls = symbols + list('@')
description_symbols = email_symobls + list(',!#$%^& ')


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
    superview = Column(Boolean, default=False)
    company = relationship('UserCompany')
    hashrate = relationship('Hashrate')

    @validates("username")
    def validate_username(self, key, username):
        username = username.lower()
        for symbol in username:
            if symbol not in symbols:
                raise HTTPException(status_code=406, detail=f"{key} contains incorrect symbols")
        return username

    @validates("email")
    def validate_email(self, key, email):
        email = email.lower()
        for symbol in email:
            if symbol not in email_symobls:
                raise HTTPException(status_code=406, detail=f"{key} contains incorrect symbols")
        spemail = email.split('@')
        if len(spemail) != 2:
            raise HTTPException(status_code=406, detail="Email is not valid")
        _, host = spemail
        host = host.split('.')
        if len(host) != 2:
            raise HTTPException(status_code=406, detail="Email is not valid")
        return email

    @validates("first_name", "last_name")
    def validate_fields(self, key, field):
        if field:
            for symbol in field.lower():
                if symbol not in symbols:
                    raise HTTPException(status_code=406, detail=f"{key} contains incorrect symbols")
        return field

    @validates("description")
    def validate_description(self, key, description):
        if description:
            for symbol in description.lower():
                if symbol not in description_symbols:
                    raise HTTPException(status_code=406,
                                        detail=f"{key} contains incorrect symbols")
        return description


class UserCompany(Base):
    __tablename__ = 'user_company'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    company_id = Column(Integer, ForeignKey('company.id'))

