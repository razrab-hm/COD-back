from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from _utils import utils
from db.schemas import companies as dto_companies, users as dto_users


def create_company_handler(auth: AuthJWT, company: dto_companies.CompanyBase, db: Session):
    utils.check_access(db, auth)
    return utils.create_company(db, company)


def create_user_handler(auth: AuthJWT, user: dto_users.UserCreate, db: Session):
    utils.check_access(db, auth)
    utils.check_email(db, user.email)
    return utils.create_user(db, user)
