from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from db.base import get_db
from db.schemas import companies as dto_companies

from _utils import handlers
router = APIRouter(prefix='/company')


@router.post('/create', response_model=dto_companies.Company)
def create_company(company: dto_companies.CompanyBase, db: Session = Depends(get_db), auth: AuthJWT = Depends()):
    return handlers.create_company_handler(auth, company, db)


# @router.post('/get', response_model=schemas.Company)
# def get_company_by_id(authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
#     current_user = authorize.get_jwt_subject()
#     company_id = user_base.get_user_by_id(db, current_user).company_id
#     if not company_id:
#         raise HTTPException(status_code=401, detail="You not in company")
#
#     company = base.get_company_by_id(db, company_id)
#     return company

