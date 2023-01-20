from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from _utils import utils
from db.schemas import companies as dto_companies, users as dto_users
from db.models import users as db_users


def create_company_handler(auth: AuthJWT, company: dto_companies.CompanyBase, db: Session):
    utils.check_access(db, auth)
    return utils.create_company(db, company)


def create_user_handler(auth: AuthJWT, user: dto_users.UserCreate, db: Session):
    utils.check_access(db, auth)
    utils.check_email_valid(user.email)
    utils.check_email_in_base(db, user.email)
    return utils.create_user(db, user)


def update_user_handler(update_data: dto_users.UserUpdate, db: Session, auth: AuthJWT):
    return utils.update_user(update_data, db, auth)

