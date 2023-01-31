from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.db import companies as db_companies
from app.models.db import users as db_users
from app.models.dto import companies as dto_companies


def create_company(db: Session, company: dto_companies.CompanyBase):
    db_company = db_companies.Company(title=company.title, contact_fio=company.contact_fio, contact_email=company.contact_email, contact_phone=company.contact_phone, img_logo=company.img_logo, description=company.description, inactive=False)
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company


def get_company_by_id(db: Session, company_id: int, access_level, user_id):
    if access_level == 1:
        return db.query(db_companies.Company).filter(db_companies.Company.id == company_id).first()
    elif access_level == 2:
        if db.query(db_users.UserCompany).filter(db_users.UserCompany.user_id == user_id).filter(db_users.UserCompany.company_id == company_id).first():
            return db.query(db_companies.Company).filter(db_companies.Company.id == company_id).first()
        else:
            return {'status': 'Deny'}
    else:
        return {'status': 'Deny'}


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


def get_companies(db, user_id, access_level):
    if access_level == 1:
        return db.query(db_companies.Company).all()
    elif access_level == 2:
        return db.query(db_companies.Company).join(db_users.UserCompany).filter(db_users.UserCompany.user_id == user_id).all()
    else:
        return []


def set_inactive_company(db: Session, company_id):
    company = db.query(db_companies.Company).filter(db_companies.Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=403, detail="Company does not exist")
    company.inactive = True
    db.commit()
    return company


def get_user_companies(user_id, db):
    return db.query(db_companies.Company).join(db_users.UserCompany).filter(db_users.UserCompany.user_id == user_id).all()

