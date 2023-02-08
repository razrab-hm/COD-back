from fastapi import HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

import app.app.auth as app_auth
import app.app.companies as app_companies
import app.app.users as app_users
import app.app.hashrates as app_hashrates
import app.app.reports as app_reports
from app.app.logger import log
from app.models.dto import (companies as dto_companies,
                        users as dto_users)
from app.models.dto import hashrates as dto_hashrates


def create_company_handler(auth: AuthJWT, company: dto_companies.CompanyBase, db: Session):
    log.input(auth, company, dto_companies, db)
    app_users.check_access(db, auth, 1)
    return app_companies.create_company(db, company)


def update_company_handler(auth: AuthJWT, company: dto_companies.CompanyUpdate, db: Session):
    log.input(auth, company, db)
    app_users.check_access(db, auth, 1)
    return app_companies.update_company(db, company)


def create_user_handler(auth: AuthJWT, user: dto_users.UserCreate, db: Session):
    log.input(auth, user, db)
    app_auth.check_email_valid(user.email)
    app_auth.check_username_in_base(db, user.username)
    app_auth.check_email_in_base(db, user.email)
    return app_users.create_user(db, user)


def update_user_handler(update_data: dto_users.UserUpdate, db: Session, auth: AuthJWT):
    log.input(update_data, db, auth)
    return app_users.update_user(update_data, db, auth)


def get_user_handler(db: Session, auth: AuthJWT):
    log.input(db, auth)
    user = app_users.get_current_user(db, auth)
    return {"username": user.username, "role": user.role}


def check_token_valid(db: Session, auth: AuthJWT):
    log.input(db, auth)
    auth.jwt_required()
    db_user = app_users.get_user_by_id(db, auth.get_jwt_subject())
    return {"message": 'success', 'role': db_user.role}


def get_all_users_handler(db: Session, auth: AuthJWT):
    log.input(db, auth)
    access_level = app_users.get_access_level(db, auth.get_jwt_subject())
    return app_users.get_all_users(db, access_level, auth.get_jwt_subject())


def set_inactive_user(db: Session, auth: AuthJWT, user_id):
    log.input(db, auth, user_id)
    root_access = app_users.get_access_level(db, auth.get_jwt_subject())
    print(auth.get_jwt_subject(), root_access)
    user_access = app_users.get_access_level(db, user_id)
    if root_access >= user_access:
        raise HTTPException(status_code=403, detail="You don't have permissions")

    return app_users.set_inactive_user(db, user_id)


def create_hashrate_handler(auth: AuthJWT, hashrate: dto_hashrates.HashrateBase, db: Session):
    log.input(auth, hashrate, db)
    app_companies.check_company_exists(db, hashrate.company_id)
    access_level = app_users.get_access_level(db, auth.get_jwt_subject())
    if access_level == 3:
        raise HTTPException(status_code=406, detail="You don't have permissions")
    if access_level == 2:
        app_companies.check_user_in_company(db, auth.get_jwt_subject(), hashrate.company_id)

    return app_hashrates.create_hashrate(db, hashrate)


def get_my_hashrates_handler(auth: AuthJWT, db):
    log.input(auth, db)
    auth.jwt_required()
    return app_hashrates.get_hashrate_by_user_id(db, auth.get_jwt_subject())


def get_company_hashrate_handler(company_id, db, auth):
    log.input(company_id, db, auth)
    access_level = app_users.get_access_level(db, auth.get_jwt_subject())
    return app_hashrates.get_hashrate_by_company_id(db, company_id, access_level, auth.get_jwt_subject())


def get_all_hashrates_handler(db, auth):
    log.input(db, auth)
    app_users.check_access(db, auth, 1)
    return app_hashrates.get_all_hashrates(db)


def get_companies_handler(db, auth):
    log.input(db, auth)
    access_level = app_users.get_access_level(db, auth.get_jwt_subject())
    return app_companies.get_companies(db, auth.get_jwt_subject(), access_level)


def get_company_by_id_handler(db, auth, company_id):
    log.input(db, auth, company_id)
    access_level = app_users.get_access_level(db, auth.get_jwt_subject())
    return app_companies.get_company_by_id(db, company_id, access_level, auth.get_jwt_subject())


def login_user_handler(db, user, auth):
    log.input(db, user, auth)
    bd_user = app_auth.check_username_in_base(db, user.username, True)
    app_auth.check_user_password(user.password, bd_user.hash_password)
    app_auth.check_inactive_account(db, bd_user.id)
    response = app_auth.create_tokens(auth, bd_user.id)
    response['role'] = bd_user.role
    return response


def refresh_handler(auth, db):
    log.input(auth, db)
    jti = auth.get_raw_jwt()['jti']
    app_auth.check_inactive_account(db, auth.get_jwt_subject())
    app_auth.check_refresh_token_is_in_blacklist(db, jti)
    app_auth.add_token_to_blacklist(db, jti)
    return app_auth.create_tokens(auth, auth.get_jwt_subject())


def set_inactive_company_handler(auth, db, company_id):
    log.input(auth, db, company_id)
    app_users.check_access(db, auth, 1)
    return app_companies.set_inactive_company(db, company_id)


def get_user_companies_handler(user_id, auth, db):
    log.input(user_id, auth, db)
    app_users.check_access(db, auth, 2)
    return app_companies.get_user_companies_full(user_id, db)


def get_my_company_handler(auth, db):
    log.input(auth, db)
    return app_companies.get_user_companies_full(auth.get_jwt_subject(), db)


def get_company_users_handler(db, company_id, auth):
    log.input(db, company_id, auth)
    access_level = app_users.get_access_level(db, auth.get_jwt_subject())
    return app_users.get_company_users(db, company_id, access_level, auth.get_jwt_subject())


def get_user_by_id_handler(db, user_id, auth):
    log.input(db, user_id, auth)
    access_level = app_users.get_access_level(db, auth.get_jwt_subject())
    return app_users.get_user_by_id(db, user_id, access_level, auth.get_jwt_subject())


def get_inactive(db, auth: AuthJWT):
    log.input(db, auth)
    app_auth.check_inactive_account(db, auth.get_jwt_subject())


def add_company_handler(company_id, user_id, auth, db):
    log.input(company_id, user_id, auth, db)
    app_users.check_access(db, auth, 1)
    return app_users.add_user_company(company_id, user_id, db)


def remove_company_handler(company_id, user_id, auth, db):
    log.input(company_id, user_id, auth, db)
    app_users.check_access(db, auth, 1)
    return app_users.remove_user_company(company_id, user_id, db)


def get_xls_handler(file, db, company_id, auth):
    log.input(file, db, company_id, auth)
    app_companies.check_company_exists(db, company_id)
    access_level = app_users.get_access_level(db, auth.get_jwt_subject())
    if access_level == 3:
        raise HTTPException(status_code=406, detail="You don't have permissions")
    if access_level == 2:
        app_companies.check_user_in_company(db, auth.get_jwt_subject(), company_id)
    return app_hashrates.get_data_from_file(file, db, company_id, auth.get_jwt_subject())


def month_day_report_handler(output_type, companies, year, month, db, auth):
    log.input(output_type, companies, year, month, db, auth)
    auth.jwt_required()
    for company in companies:
        app_companies.check_company_exists(db, company)
    if app_users.get_access_level(db, auth.get_jwt_subject()) != 1:
        app_users.check_user_in_companies(db, auth.get_jwt_subject(), companies)
    return app_reports.month_day_report(db, companies, year, month, output_type)


def year_quarter_month_report_handler(output_type, companies, year, db, auth):
    log.input(output_type, companies, year, db, auth)
    auth.jwt_required()
    for company in companies:
        app_companies.check_company_exists(db, company)
    if app_users.get_access_level(db, auth.get_jwt_subject()) != 1:
        app_users.check_user_in_companies(db, auth.get_jwt_subject(), companies)
    return app_reports.year_quarter_month_report(db, companies, year, output_type)


def year_quarter_report_handler(output_type, companies, year, db, auth):
    log.input(output_type, companies, year, db, auth)
    auth.jwt_required()
    for company in companies:
        app_companies.check_company_exists(db, company)
    if app_users.get_access_level(db, auth.get_jwt_subject()) != 1:
        app_users.check_user_in_companies(db, auth.get_jwt_subject(), companies)
    return app_reports.year_quarter_report(db, companies, year, output_type)


def year_quarter_month_day_report_handler(output_type, companies, year, db, auth):
    log.input(output_type, companies, year, db, auth)
    auth.jwt_required()
    for company in companies:
        app_companies.check_company_exists(db, company)
    if app_users.get_access_level(db, auth.get_jwt_subject()) != 1:
        app_users.check_user_in_companies(db, auth.get_jwt_subject(), companies)
    return app_reports.year_quarter_month_day_report(db, companies, year, output_type)


def quarter_month_report_handler(output_type, companies, year, quarter, db, auth):
    log.input(output_type, companies, year, quarter, db, auth)
    auth.jwt_required()
    for company in companies:
        app_companies.check_company_exists(db, company)
    if app_users.get_access_level(db, auth.get_jwt_subject()) != 1:
        app_users.check_user_in_companies(db, auth.get_jwt_subject(), companies)
    return app_reports.quarter_month_report(db, companies, year, quarter, output_type)


def quarter_month_day_report_handler(output_type, companies, year, quarter, db, auth):
    log.input(output_type, companies, year, quarter, db, auth)
    auth.jwt_required()
    for company in companies:
        app_companies.check_company_exists(db, company)
    if app_users.get_access_level(db, auth.get_jwt_subject()) != 1:
        app_users.check_user_in_companies(db, auth.get_jwt_subject(), companies)
    return app_reports.quarter_month_day_report(db, companies, year, quarter, output_type)


def logout_handler(db, auth):
    log.input(db, auth)
    auth.jwt_required()
    jti = auth.get_raw_jwt()['jti']
    app_auth.add_token_to_blacklist(db, jti)
    return {'status': 'ok'}


def get_dates_handler(auth, db):
    log.input(auth, db)
    auth.jwt_required()
    return app_hashrates.get_dates(db)


def update_user_companies_handler(user_id, companies_id, auth, db):
    log.input(user_id, companies_id, auth, db)
    auth.jwt_required()
    access_level = app_users.get_access_level(db, auth.get_jwt_subject())
    return app_users.update_user_companies(db, companies_id, user_id, access_level, auth.get_jwt_subject())

