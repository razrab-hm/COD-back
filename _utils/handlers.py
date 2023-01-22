from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from _utils import utils
from db.schemas import (companies as dto_companies,
                        users as dto_users,
                        hashrates as dto_hashrates)
from db.models import users as db_users


def create_company_handler(auth: AuthJWT, company: dto_companies.CompanyBase, db: Session):
    utils.check_access(db, auth)
    return utils.create_company(db, company)


def update_company_handler(auth: AuthJWT, company: dto_companies.CompanyUpdate, db: Session):
    utils.check_access(db, auth)
    return utils.update_company(db, company)


def create_user_handler(auth: AuthJWT, user: dto_users.UserCreate, db: Session):
    utils.check_access(db, auth)
    utils.check_email_valid(user.email)
    utils.check_email_in_base(db, user.email)
    return utils.create_user(db, user)


def update_user_handler(update_data: dto_users.UserUpdate, db: Session, auth: AuthJWT):
    return utils.update_user(update_data, db, auth)


def get_user_handler(db: Session, auth: AuthJWT):
    auth.jwt_required()
    return utils.get_user_by_id(db, auth.get_jwt_subject())


def get_all_user_handler(db: Session, auth: AuthJWT):
    utils.check_access(db, auth)
    print(len(db.query(db_users.User).all()))
    return db.query(db_users.User).all()


def block_user_handler(db: Session, auth: AuthJWT, user_id):
    utils.check_access(db, auth)
    return utils.ban_user(db, user_id)


def create_hashrate_handler(auth: AuthJWT, hashrate: dto_hashrates.HashrateBase, db: Session):
    utils.check_access(db, auth)
    return utils.create_hash(db, hashrate)


def get_company_handler(company, db, auth):
    auth.jwt_required()
    return utils.get_company_by_id(db, company.id)


