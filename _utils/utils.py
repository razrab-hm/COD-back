from fastapi import HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from db.schemas import (companies as dto_companies,
                        hashrates as dto_hashrates,
                        users as dto_users)
from db.models import (companies as db_companies,
                       hashrates as db_hashrates,
                       users as db_users)


def create_super_user(db, username, password):
    user = db_users.User(email=username, hash_password=password + 'notreallyhashed', role='root', inactive=False)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_company(db: Session, company: dto_companies.CompanyBase):
    db_company = db_companies.Company(name=company.name, contact_name=company.contact_name, contact_email=company.contact_email, inactive=False)
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company


def get_company_by_id(db: Session, company_id: int):
    return db.query(db_companies.Company).filter(db_companies.Company.id == company_id).first()


def update_company(db: Session, update_data):
    company = db.query(db_companies.Company).filter(db_companies.Company.id == update_data.id).first()
    if update_data.title:
        company.name = update_data.name
    if update_data.contact_fio:
        company.contact_name = update_data.contact_name
    if update_data.contact_email:
        company.contact_email = update_data.contact_email
    if update_data.img_logo:
        company.img_logo = update_data.img_logo
    if update_data.contact_phone:
        company.contact_phone = update_data.contact_phone
    if update_data.description:
        company.description = update_data.description
    db.commit()
    return company


def create_hash(db: Session, hash: dto_hashrates.HashrateBase):
    db_hash = db_hashrates.Hashrate(date=hash.date, average=hash.average, hash=hash.hash, company_id=hash.company_id)
    db.add(db_hash)
    db.commit()
    db.refresh(db_hash)
    return db_hash


def get_hash_by_company_id(db: Session, id: int):
    return db.query(db_hashrates.Hashrate).filter(db_hashrates.Hashrate.company_id == id).all()


def get_user_by_email(db: Session, email: str):
    return db.query(db_users.User).filter(db_users.User.email == email).first()


def get_user_by_id(db: Session, id: int):
    return db.query(db_users.User).filter(db_users.User.id == id).first()


def create_user(db: Session, user: dto_users.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = db_users.User(email=user.email, hash_password=fake_hashed_password, role=user.role, inactive=False)
    if user.company_id:
        db_user.company_id = user.company_id
    db.add(db_user)
    try:
        db.commit()
    except IntegrityError as e:
        print(e)
        raise HTTPException(status_code=403, detail="Company not registered!")
    db.refresh(db_user)
    return db_user


def set_user_company(db: Session, email: str, company_id: int):
    req = db.query(db_users.User).filter(db_users.User.email == email).update({'company_id': company_id})
    db.commit()
    return req


def get_current_user(db, auth: AuthJWT):
    auth.jwt_required()
    current_user = get_user_by_id(db, auth.get_jwt_subject())
    return current_user


def check_access(db, auth: AuthJWT, permission_level='root'):
    user = get_current_user(db, auth)
    if permission_level == 'root':
        if not user.role == permission_level:
            raise HTTPException(status_code=405, detail=f"You don't have permissions. You: {user.role}")
    else:
        if user.role == 'manager':
            if user.role == permission_level:
                raise HTTPException(status_code=405, detail=f"You don't have permissions. You: {user.role}")


def check_email_in_base(db, email):
    if get_user_by_email(db, email):
        raise HTTPException(status_code=400, detail="Email already registered")


def check_email_valid(email):
    email = email.split('@')
    if len(email) != 2:
        raise HTTPException(status_code=403, detail="Email is not valid")
    _, host = email
    host = host.split('.')
    if len(host) != 2:
        raise HTTPException(status_code=403, detail="Email is not valid")


def update_user(update_data, db: Session, auth):
    if update_data.company_id or update_data.role == 'root':
        check_access(db, auth)
    elif update_data.email or update_data.role:
        check_access(db, auth, 'admin')
    else:
        if update_data.id != auth.get_jwt_subject() and get_current_user(db, auth).role == 'manager':
            HTTPException(status_code=405, detail="You can't manage password to other user")

    user = db.query(db_users.User).filter(db_users.User.id == update_data.id).first()

    if update_data.email:
        user.email = update_data.email
    if update_data.company_id:
        user.company_id = update_data.company_id
    if update_data.role:
        user.role = update_data.role
    db.commit()
    return user


def ban_user(db: Session, user_id):
    user = db.query(db_users.User).filter(db_users.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=403, detail="User does not exist")
    user.inactive = True
    db.commit()
    return user


@AuthJWT.load_config
def get_config():
    return dto_users.Settings()

