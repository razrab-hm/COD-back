import hashlib

from fastapi import HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.db import companies as db_companies
from app.models.db import users as db_users
from app.models.dto import users as dto_users


def get_user_by_username(db: Session, username: str):
    return db.query(db_users.User).filter(db_users.User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(db_users.User).filter(db_users.User.email == email).first()


def get_user_by_id(db: Session, user_id: int, access_level=None, from_user_id=None):
    if (not access_level and not from_user_id) or access_level == 1:
        return db.query(db_users.User).filter(db_users.User.id == user_id).first()
    else:
        if access_level == 2:
            companies_id = db.query(db_users.UserCompany.company_id).filter(db_users.UserCompany.user_id == from_user_id).all()
            for company_id in companies_id:
                user = db.query(db_users.User).filter(db_users.UserCompany.company_id == company_id[0]).filter(db_users.UserCompany.user_id == user_id).first()
                if user:
                    return user
            raise HTTPException(status_code=406, detail="User not in yours company!")
        else:
            pass


def add_user_company(company_id, user_id, db):
    data = db.query(db_users.UserCompany).filter(db_users.UserCompany.company_id == company_id).filter(db_users.UserCompany.user_id == user_id).first()
    if data:
        raise HTTPException(status_code=406, detail="User already in group")
    user_company = db_users.UserCompany(user_id=user_id, company_id=company_id)
    db.add(user_company)
    db.commit()
    return {'status': '+ company'}


def remove_user_company(company_id, user_id, db):
    obj = db.query(db_users.UserCompany).filter(db_users.UserCompany.company_id == company_id).filter(db_users.UserCompany.user_id == user_id).delete()
    db.commit()
    if obj:
        return {'status': '- company'}
    else:
        return {'status': 'failed'}


def get_current_user(db, auth: AuthJWT):
    auth.jwt_required()
    current_user = get_user_by_id(db, auth.get_jwt_subject())
    return current_user


def check_access(db, auth: AuthJWT, needed):
    access_level = get_access_level(db, auth.get_jwt_subject())
    if access_level > needed:
        raise HTTPException(status_code=406, detail="You don't have permissions")


def get_access_level(db, user_id):
    role = db.query(db_users.User.role).filter(db_users.User.id == user_id).first()
    if not role:
        raise HTTPException(status_code=406, detail="Not authorizated")
    role = role[0]
    return 1 if role == 'root' else 2 if role == 'admin' else 3


def update_user(update_data, db: Session, auth):
    if update_data.role == 'root':
        check_access(db, auth, 1)
    elif update_data.email or update_data.role == 'admin':
        check_access(db, auth, 2)
    else:
        if update_data.id != auth.get_jwt_subject() and get_current_user(db, auth).role == 'manager':
            HTTPException(status_code=405, detail="You can't manage password to other user")

    user = db.query(db_users.User).filter(db_users.User.id == update_data.id).first()

    if update_data.email:
        user.email = update_data.email
    if update_data.role:
        user.role = update_data.role
    if update_data.password:
        user.password = hashlib.md5(update_data.password.encode('utf-8'))
    db.commit()
    return user


def set_inactive_user(db: Session, user_id):
    user = db.query(db_users.User).filter(db_users.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=403, detail="User does not exist")
    user.inactive = True
    db.commit()
    return user


def create_user(db: Session, user: dto_users.UserCreate):
    hashed_password = hashlib.md5(user.password.encode('utf-8')).hexdigest()
    db_user = db_users.User(email=user.email, hash_password=hashed_password, role='manager', inactive=False, username=user.username)
    db.add(db_user)
    db.commit()
    return {'username': db_user.username, 'role': db_user.role}


def get_company_users(db, company_id, access_level, from_user_id):
    if access_level == 1:
        return db.query(db_users.User).join(db_users.UserCompany).filter(db_users.UserCompany.company_id == company_id).all()
    elif access_level == 2:
        if db.query(db_users.User).join(db_users.UserCompany).filter(db_users.UserCompany.company_id == company_id).filter(db_users.UserCompany.user_id == from_user_id).first():
            return db.query(db_users.User).join(db_users.UserCompany).filter(db_users.UserCompany.company_id == company_id).all()
    else:
        return []


def get_all_users(db, access_level, user_id):
    if access_level == 1:
        return db.query(db_users.User).all()
    elif access_level == 2:
        companies_id = db.query(db_users.User).filter(db_users.UserCompany.user_id == user_id).all()
        users = []
        for company_id in companies_id:
            users.extend(db.query(db_users.User).filter(db_users.UserCompany.company_id == company_id[0]).all())
        return users
    else:
        return []

