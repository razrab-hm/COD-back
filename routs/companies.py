from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from db.base import get_db
from db.schemas import companies as dto_companies

from app import handlers

router = APIRouter(prefix='/companies')


@router.post('/create', response_model=dto_companies.Company)
def create_company(company: dto_companies.CompanyBase, db: Session = Depends(get_db), auth: AuthJWT = Depends()):
    return handlers.create_company_handler(auth, company, db)


@router.put('/update', response_model=dto_companies.Company)
def update_company(company: dto_companies.CompanyUpdate, db: Session = Depends(get_db), auth: AuthJWT = Depends()):
    return handlers.update_company_handler(auth, company, db)


@router.get('/get', response_model=dto_companies.Company)
def get_company(company: dto_companies.CompanyRead, db: Session = Depends(get_db), auth: AuthJWT = Depends()):
    return handlers.get_company_handler(company, db, auth)


@router.delete('/inactive', response_model=dto_companies.Company)
def set_inactive_company(company_id: int, auth: AuthJWT = Depends(), db: Session = Depends(get_db)):
    return handlers.block_company_handler(auth, db, company_id)


@router.get('/{user_id}/companies')
def get_user_companies(user_id: int, auth: AuthJWT = Depends(), db: Session = Depends(get_db)):
    # return handlers.get_user_companies_handler(user, auth, db)
    pass

# @router.post('/get', response_model=schemas.Company)
# def get_company_by_id(authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
#     current_user = authorize.get_jwt_subject()
#     company_id = user_base.get_user_by_id(db, current_user).company_id
#     if not company_id:
#         raise HTTPException(status_code=401, detail="You not in company")
#
#     company = base.get_company_by_id(db, company_id)
#     return company

