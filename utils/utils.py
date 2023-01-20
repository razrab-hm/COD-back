from fastapi import HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from db.schemas import (companies as dto_companies,
                        hashrates as dto_hashrates,
                        permissions as dto_permissions,
                        users as dto_users)
from db.models import (companies as db_companies,
                       hashrates as db_hashrates,
                       permissions as db_permissions,
                       users as db_users)


def create_company(db: Session, company: dto_companies.CompanyBase):
    db_company = db_companies.Company(name=company.name, contact_name=company.contact_name, contact_email=company.contact_email)
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company


def get_company_by_id(db: Session, company_id: int):
    return db.query(db_companies.Company).filter(db_companies.Company.id == company_id).first()


def create_hash(db: Session, hash: dto_hashrates.HashrateBase):
    db_hash = db_hashrates.Hashrate(date=hash.date, average=hash.average, hash=hash.hash, company_id=hash.company_id)
    db.add(db_hash)
    db.commit()
    db.refresh(db_hash)
    return db_hash


def get_hash_by_company_id(db: Session, id: int):
    return db.query(db_hashrates.Hashrate).filter(db_hashrates.Hashrate.company_id == id).all()


def create_permission(db: Session, permission: dto_permissions.PermissionBase):
    db_permission = db_permissions.Permission(permission_name=permission.permission_name)
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    return db_permission


def get_permission_name(db: Session, permission_id):
    return db.query(db_permissions.Permission).filter(db_permissions.Permission.id == permission_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(db_users.User).filter(db_users.User.email == email).first()


def get_user_by_id(db: Session, id: int):
    return db.query(db_users.User).filter(db_users.User.id == id).first()


def create_user(db: Session, user: dto_users.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = db_users.User(email=user.email, hash_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def set_user_company(db: Session, email: str, company_id: int):
    req = db.query(db_users.User).filter(db_users.User.email == email).update({'company_id': company_id})
    db.commit()
    return req


def check_user_permission_id(db, user_id):
    current_user = get_user_by_id(db, user_id)
    user_permission_id = current_user.permission_id
    return user_permission_id


def check_permissions(db, auth: AuthJWT, permission_level=1):
    auth.jwt_required()
    permission_id = check_user_permission_id(db, auth.get_jwt_subject())
    if not permission_id <= permission_level:
        raise HTTPException(status_code=401, detail="You don't have permissions")


@AuthJWT.load_config
def get_config():
    return dto_users.Settings()

