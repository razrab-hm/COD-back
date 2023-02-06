from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from app.app.db import get_db
from app.models.dto import companies as dto_companies
from app.app import handlers

router = APIRouter(prefix='/companies', tags=["companies"])


@router.post('/', status_code=201)
def create_company(company: dto_companies.CompanyBase, db: Session = Depends(get_db), auth: AuthJWT = Depends()):
    return handlers.create_company_handler(auth, company, db)


@router.put('/')
def update_company(company: dto_companies.CompanyUpdate, db: Session = Depends(get_db), auth: AuthJWT = Depends()):
    return handlers.update_company_handler(auth, company, db)


@router.get('/')
def get_company(db: Session = Depends(get_db), auth: AuthJWT = Depends()):
    return handlers.get_companies_handler(db, auth)


@router.get('/company/{company_id}')
def get_company(company_id: int, db: Session = Depends(get_db), auth: AuthJWT = Depends()):
    return handlers.get_company_by_id_handler(db, auth, company_id)


@router.delete('/{company_id}', status_code=205)
def set_inactive_company(company_id: int, auth: AuthJWT = Depends(), db: Session = Depends(get_db)):
    return handlers.set_inactive_company_handler(auth, db, company_id)


@router.get('/user/{user_id}')
def get_user_companies(user_id: int, auth: AuthJWT = Depends(), db: Session = Depends(get_db)):
    return handlers.get_user_companies_handler(user_id, auth, db)


@router.get('/me')
def get_my_companies(auth: AuthJWT = Depends(), db: Session = Depends(get_db)):
    return handlers.get_my_company_handler(auth, db)


