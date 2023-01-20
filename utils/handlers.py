from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from utils.utils import check_permissions, create_company
from db.schemas import companies as dto_companies


def create_company_handler(auth: AuthJWT, company: dto_companies.CompanyBase, db: Session):
    check_permissions(db, auth)
    return create_company(db, company)
