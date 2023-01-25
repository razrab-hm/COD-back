from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

import app.auth as app_auth
import app.companies as app_companies
import app.users as app_users
import app.hashrates as app_hashrates
from models.dto import (companies as dto_companies,
                        users as dto_users,
                        hashrates as dto_hashrates)
from models.db import users as db_users


def create_company_handler(auth: AuthJWT, company: dto_companies.CompanyBase, db: Session):
    app_users.check_access(db, auth, 1)
    return app_companies.create_company(db, company)


def update_company_handler(auth: AuthJWT, company: dto_companies.CompanyUpdate, db: Session):
    app_users.check_access(db, auth, 1)
    return app_companies.update_company(db, company)


def create_user_handler(auth: AuthJWT, user: dto_users.UserCreate, db: Session):
    # app_users.check_access(db, auth, 1)
    app_auth.check_email_valid(user.email)
    app_auth.check_username_in_base(db, user.username)
    return app_users.create_user(db, user)


def update_user_handler(update_data: dto_users.UserUpdate, db: Session, auth: AuthJWT):
    return app_users.update_user(update_data, db, auth)


def get_user_handler(db: Session, auth: AuthJWT):
    user = app_users.get_current_user(db, auth)
    return {"username": user.username, "role": user.role}


def check_token_valid(db: Session, auth: AuthJWT):
    auth.jwt_required()
    return {"message": 'success'}


def get_all_users_handler(db: Session, auth: AuthJWT):
    access_level = app_users.get_access_level(db, auth.get_jwt_subject())
    return app_users.get_all_users(db, access_level, auth.get_jwt_subject())


def set_inactive_user(db: Session, auth: AuthJWT, user_id):
    app_users.check_access(db, auth, 1)
    return app_users.set_inactive_user(db, user_id)


def create_hashrate_handler(auth: AuthJWT, hashrate: dto_hashrates.HashrateBase, db: Session):
    app_users.check_access(db, auth, 1)
    return app_hashrates.create_hashrate(db, hashrate)


def get_my_hashrates_handler(auth: AuthJWT, db):
    auth.jwt_required()
    return app_hashrates.get_hashrate_by_user_id(db, auth.get_jwt_subject())


def get_company_hashrate_handler(company_id, db, auth):
    access_level = app_users.get_access_level(db, auth.get_jwt_subject())
    # return app_hashrates.get_hashrate_by_company_id(db, company_id, access_level)


def get_all_hashrates_handler(db, auth):
    app_users.check_access(db, auth, 1)
    return app_hashrates.get_all_hashrates(db)


def get_companies_handler(db, auth):
    access_level = app_users.get_access_level(db, auth.get_jwt_subject())
    return app_companies.get_companies(db, auth.get_jwt_subject(), access_level)


def get_company_by_id_handler(db, auth, company_id):
    access_level = app_users.get_access_level(db, auth.get_jwt_subject())
    return app_companies.get_company_by_id(db, company_id, access_level, auth.get_jwt_subject())


def login_user_handler(db, user, auth):
    bd_user = app_auth.check_username_in_base(db, user.username, True)
    app_auth.check_user_password(user.password, bd_user.hash_password)
    return app_auth.create_tokens(auth, bd_user.id)


def refresh_handler(auth, db):
    jti = auth.get_raw_jwt()['jti']
    app_auth.check_refresh_token_is_in_blacklist(db, jti)
    app_auth.add_token_to_blacklist(db, jti)
    return app_auth.create_tokens(auth, auth.get_jwt_subject())


def set_inactive_company_handler(auth, db, company_id):
    app_users.check_access(db, auth, 1)
    return app_companies.set_inactive_company(db, company_id)


def get_user_companies_handler(user_id, auth, db):
    app_users.check_access(db, auth, 1)
    return app_companies.get_user_companies(user_id, db)


def get_my_company_handler(auth, db):
    return app_companies.get_user_companies(auth.get_jwt_subject(), db)


def get_company_users_handler(db, company_id, auth):
    access_level = app_users.get_access_level(db, auth.get_jwt_subject())
    return app_users.get_company_users(db, company_id, access_level, auth.get_jwt_subject())


def get_user_by_id_handler(db, user_id, auth):
    access_level = app_users.get_access_level(db, auth.get_jwt_subject())
    return app_users.get_user_by_id(db, user_id, access_level, auth.get_jwt_subject())


def add_company_handler(company_id, user_id, auth, db):
    app_users.check_access(db, auth, 1)
    return app_users.add_user_company(company_id, user_id, db)


def remove_company_handler(company_id, user_id, auth, db):
    app_users.check_access(db, auth, 1)
    return app_users.remove_user_company(company_id, user_id, db)


def get_xls_handler(file, db, company_id, auth):
    app_users.check_access(db, auth, 1)
    return app_hashrates.get_data_from_file(file, db, company_id, auth.get_jwt_subject())


def get_report_handler(file_format, company_id, from_date, to_date, auth, year, db):
    return app_hashrates.get_report(db, file_format, company_id, from_date, to_date, auth, year)


def get_report_by_type_handler(report_type, year, month, db, auth):
    auth.jwt_required()
    return app_hashrates.get_func_by_report_type[report_type](db, year, month)

