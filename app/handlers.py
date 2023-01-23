from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

import app.auth as app_auth
import app.companies as app_companies
import app.users as app_users
from app import utils
from db.schemas import (companies as dto_companies,
                        users as dto_users,
                        hashrates as dto_hashrates)
from db.models import users as db_users


def create_company_handler(auth: AuthJWT, company: dto_companies.CompanyBase, db: Session):
    app_users.check_access(db, auth)
    return app_companies.create_company(db, company)


def update_company_handler(auth: AuthJWT, company: dto_companies.CompanyUpdate, db: Session):
    app_users.check_access(db, auth)
    return app_companies.update_company(db, company)


def create_user_handler(auth: AuthJWT, user: dto_users.UserCreate, db: Session):
    app_users.check_access(db, auth, 1)
    app_auth.check_email_valid(user.email)
    app_auth.check_email_in_base(db, user.email)
    return app_users.create_user(db, user)


def update_user_handler(update_data: dto_users.UserUpdate, db: Session, auth: AuthJWT):
    return app_users.update_user(update_data, db, auth)


def get_user_handler(db: Session, auth: AuthJWT):
    return app_users.get_current_user(db, auth)


def get_all_users_handler(db: Session, auth: AuthJWT):
    access_level = app_users.get_access_level(db, auth.get_jwt_subject())
    return app_users.get_all_users(db, access_level, auth.get_jwt_subject())


def set_inactive_user(db: Session, auth: AuthJWT, user_id):
    app_users.check_access(db, auth, 1)
    return app_users.set_inactive_user(db, user_id)


def create_hashrate_handler(auth: AuthJWT, hashrate: dto_hashrates.HashrateBase, db: Session):
    app_users.check_access(db, auth)
    return utils.create_hash(db, hashrate)


def get_company_handler(company, db, auth):
    auth.jwt_required()
    return app_companies.get_company_by_id(db, company.id)


def login_user_handler(db, user, auth):
    bd_user = app_auth.check_email_in_base(db, user.email, True)
    app_auth.check_user_password(user.password, bd_user.hash_password)
    return app_auth.create_tokens(auth, bd_user)


def refresh_handler(auth, db):
    user = app_users.get_current_user(db, auth)
    app_auth.check_refresh_token_is_in_blacklist(db, auth)
    return app_auth.create_tokens(auth, user)


def block_company_handler(auth, db, company_id):
    app_users.check_access(db, auth)
    return app_companies.block_company(db, company_id)


def get_user_companies_handler(user, auth, db):
    auth.jwt_required()
    return app_users.get_user_companies(user.id, db)


def get_company_users_handler(db, company_id, auth):
    access_level = app_users.get_access_level(db, auth.get_jwt_subject())
    return app_users.get_company_users(db, company_id, access_level, auth.get_jwt_subject())


def get_user_by_id_handler(db, user_id, auth):
    access_level = app_users.get_access_level(db, auth.get_jwt_subject())
    return app_users.get_user_by_id(db, user_id, access_level, auth.get_jwt_subject())


def add_company_handler(company_id, user_id, auth, db):
    app_users.check_access(db, auth, 1)
    return app_users.add_user_company(company_id, user_id, db)
