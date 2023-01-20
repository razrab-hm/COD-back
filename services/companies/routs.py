from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core.base import get_db
from services.companies import schemas, base
from services.users import base as user_base
from services.users.schemas import UserBase

router = APIRouter(prefix='/company')


@router.post('/create', response_model=schemas.Company)
def create_company(company: schemas.CompanyBase, db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    authorize.jwt_required()

    current_user = authorize.get_jwt_subject()
    user_permission = user_base.get_user_by_id(db, current_user).permission_id

    if not user_permission < 3:
        raise HTTPException(status_code=401, detail="You don't have permissions")
    return base.create_company(db, company)


@router.post('/get', response_model=schemas.Company)
def get_company_by_id(authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    current_user = authorize.get_jwt_subject()
    company_id = user_base.get_user_by_id(db, current_user).company_id
    if not company_id:
        raise HTTPException(status_code=401, detail="You not in company")

    company = base.get_company_by_id(db, company_id)
    return company

