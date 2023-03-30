from fastapi import HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.app import users as app_users
from app.app.logger import log
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
        if check_user_in_company(db, user_id, company_id):
            return db.query(db_companies.Company).filter(db_companies.Company.id == company_id).first()
        else:
            raise HTTPException(status_code=406, detail="You don't have permissions")
    else:
        raise HTTPException(status_code=406, detail="You don't have permissions")


def update_company(db: Session, update_data, access_level, user_id):
    log.input(db, update_data)
    company = db.query(db_companies.Company).filter(db_companies.Company.id == update_data.id).first()
    if access_level == 2:
        check_user_in_company(db, user_id, update_data.id)
        if company.inactive:
            raise HTTPException(status_code=406, detail="You don't have permissions")
        if update_data.inactive.lower() == 'true':
            raise HTTPException(status_code=406, detail="You don't have permissions")
    elif access_level == 3:
        raise HTTPException(status_code=406, detail="You don't have permissions")

    if update_data.title:
        company.title = update_data.title
    # if update_data.contact_fio:
    company.contact_fio = update_data.contact_fio
    if update_data.contact_email:
        company.contact_email = update_data.contact_email
    # if update_data.img_logo:
    #     company.img_logo = update_data.img_logo
    # if update_data.contact_phone:
    company.contact_phone = update_data.contact_phone
    # if update_data.description:
    company.description = update_data.description
    if update_data.inactive:
        if update_data.inactive.lower() == 'true':
            company.inactive = True
        else:
            company.inactive = False

    db.commit()
    db.refresh(company)
    log.output(company)
    return company


def get_companies(db, user_id, access_level, inactive):
    log.input(db, user_id, access_level)
    if access_level == 1:
        query = db.query(db_companies.Company)
        if inactive:
            query = query.filter(db_companies.Company.inactive == True)
        return query.all()
    elif access_level == 2:
        query = db.query(db_companies.Company).join(db_users.UserCompany).filter(db_users.UserCompany.user_id == user_id)
        if inactive:
            query = query.filter(db_companies.Company.inactive == True)
        return query.all()
    else:
        return []


def check_company_exists(db, company_id):
    log.input(db, company_id)
    company = db.query(db_companies.Company).filter(db_companies.Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=403, detail="Company does not exist")


def set_inactive_company(db: Session, company_id):
    log.input(db, company_id)
    company = db.query(db_companies.Company).filter(db_companies.Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=403, detail="Company does not exist")
    company.inactive = True
    db.commit()
    db.refresh(company)
    log.output(company)
    return company


def get_user_companies(user_id, db):
    log.input(user_id, db)
    companies = db.query(db_companies.Company).join(db_users.UserCompany).filter(db_users.UserCompany.user_id == user_id).filter(db_companies.Company.inactive != True).all()
    log.output(companies)
    return [company.id for company in companies]


def get_user_companies_with_inactive(user_id, db):
    log.input(user_id, db)
    companies = db.query(db_companies.Company).join(db_users.UserCompany).filter(db_users.UserCompany.user_id == user_id).all()
    log.output(companies)
    return [company.id for company in companies]


def get_user_companies_full_me(user_id, db):
    if app_users.get_access_level(db, user_id) == 1:
        companies = db.query(db_companies.Company).all()
        return companies

    log.input(user_id, db)
    companies = db.query(db_companies.Company).join(db_users.UserCompany).filter(db_users.UserCompany.user_id == user_id).filter(db_companies.Company.inactive != True).all()
    log.output(companies)
    return companies


def get_user_companies_full_admin(user_id, db):
    if app_users.get_access_level(db, user_id) == 1:
        companies = db.query(db_companies.Company).all()
        return companies

    log.input(user_id, db)
    companies = db.query(db_companies.Company).join(db_users.UserCompany).filter(db_users.UserCompany.user_id == user_id).all()
    log.output(companies)
    return companies


def check_user_in_company(db, user_id, company_id):
    log.input(db, user_id, company_id)
    user_company = db.query(db_users.UserCompany).join(db_companies.Company).filter(and_(db_users.UserCompany.user_id == user_id, db_users.UserCompany.company_id == company_id)).first()
    if not user_company:
        raise HTTPException(status_code=406, detail="You don't have permissions")
    return True


def update_company_users(db, users_id, company_id, access_level, user_id):
    log.input(db, users_id, company_id, access_level, user_id)
    if access_level == 2:
        check_user_in_company(db, user_id, company_id)
    elif access_level == 3:
        raise HTTPException(status_code=406, detail="You don't have permissions")

    db.query(db_users.UserCompany).filter(db_users.UserCompany.company_id == company_id).delete()
    db.commit()

    response = []

    for i in users_id:
        obj = db_users.UserCompany(user_id=i, company_id=company_id)
        response.append(obj)
        db.add(obj)

    db.commit()

    return {'updated_users': response}


def get_company_by_name(company_name, db):
    return db.query(db_companies.Company).filter(db_companies.Company.title == company_name).first()

