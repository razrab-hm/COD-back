import string

from fastapi import HTTPException
from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy.orm import relationship, validates

from app.app.db import Base


symbols = list(string.ascii_lowercase) + list('0123456789_-.') + list(string.ascii_uppercase) + [' ']
email_symobls = list(string.ascii_lowercase) + list('0123456789_-.') + list('@')
phone_symbols = list('0123456789-()+ ')
description_symbols = email_symobls + list(',!#$%^& ')


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

    @validates("title", "contact_fio")
    def validate_title(self, key, field):
        for symbol in field:
            if symbol not in symbols:
                raise HTTPException(status_code=406, detail="Symbols in your fields not ascii symbols or numerics")
        return field

    @validates("contact_email")
    def validate_email(self, key, email):
        email = email.lower()
        for symbol in email:
            if symbol not in email_symobls:
                raise HTTPException(status_code=406, detail="Symbols in your email not ascii symbols or numerics")
        spemail = email.split('@')
        if len(spemail) != 2:
            raise HTTPException(status_code=406, detail="Email is not valid")
        _, host = spemail
        host = host.split('.')
        if len(host) != 2:
            raise HTTPException(status_code=406, detail="Email is not valid")
        return email

    @validates("contact_phone")
    def validate_phone(self, key, phone):
        for symbol in phone:
            if symbol not in phone_symbols:
                raise HTTPException(status_code=406, detail="Phone incorrect")
        return phone

    @validates("description")
    def validate_description(self, key, description):
        description = description.lower()
        for symbol in description:
            if symbol not in description_symbols:
                raise HTTPException(status_code=406, detail="Description symbols incorrect")
        return description
