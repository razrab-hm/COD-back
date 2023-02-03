import hashlib

from app.models.db import users, companies, auth, hashrates
from app.app import db as core_db
from app.tests import company_creator


def user(username='user', email='user@mail.ru', company=None):
    db = core_db.get_core_db()

    db_user = users.User(username=username,
                         email=email,
                         hash_password=hashlib.md5('qwerty'.encode('utf-8')).hexdigest(),
                         role='manager', inactive=False)

    db.add(db_user)
    db.commit()

    if company:
        user_company = users.UserCompany(company_id=company, user_id=db_user.id)
        db.add(user_company)
        db.commit()
        db.refresh(user_company)

    db.refresh(db_user)
    db.close()
    return db_user


def root_user(username='root_user', email='root_user@mail.ru', company=None):
    db = core_db.get_core_db()

    db_user = users.User(username=username,
                         email=email,
                         hash_password=hashlib.md5('qwerty'.encode('utf-8')).hexdigest(),
                         role='root', inactive=False)

    db.add(db_user)
    db.commit()

    if company:
        user_company = users.UserCompany(company_id=company, user_id=db_user.id)
        db.add(user_company)
        db.commit()
        db.refresh(user_company)

    db.refresh(db_user)
    db.close()

    return db_user


def admin_user(username='admin_user', email='admin_user@mail.ru', company=None):
    db = core_db.get_core_db()

    db_user = users.User(username=username,
                         email=email,
                         hash_password=hashlib.md5('qwerty'.encode('utf-8')).hexdigest(),
                         role='admin', inactive=False)

    db.add(db_user)
    db.commit()

    if company:
        user_company = users.UserCompany(company_id=company, user_id=db_user.id)
        db.add(user_company)
        db.commit()
        db.refresh(user_company)

    db.refresh(db_user)
    db.close()
    return db_user


def inactive_user():
    db = core_db.get_core_db()

    db_user = users.User(username='inactive_user',
                         email='inactive_user@mail.ru',
                         hash_password=hashlib.md5('qwerty'.encode('utf-8')).hexdigest(),
                         role='manager', inactive=True)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db.close()
    return db_user


