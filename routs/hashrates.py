from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Body
from fastapi_jwt_auth import AuthJWT
from pydantic.types import date
from sqlalchemy.orm import Session

import app.hashrates
import app.users
from app import handlers
from app.db import get_db
from models.dto import hashrates as dto_hashrates

router = APIRouter(prefix='/hashrates')


@router.post('/', response_model=dto_hashrates.Hashrate)
def create_hash(hashrate: dto_hashrates.HashrateBase, db: Session = Depends(get_db), auth: AuthJWT = Depends()):
    return handlers.create_hashrate_handler(auth, hashrate, db)


@router.get('/')
def get_all_hashrates(db: Session = Depends(get_db), auth: AuthJWT = Depends()):
    return handlers.get_all_hashrates_handler(db, auth)


@router.get('/company/{company_id}')
def get_company_hashrates(company_id: int, db: Session = Depends(get_db), auth: AuthJWT = Depends()):
    return handlers.get_company_hashrate_handler(company_id, db, auth)


@router.get('/me')
def get_my_hashrates(auth: AuthJWT = Depends(), db: Session = Depends(get_db)):
    return handlers.get_my_hashrates_handler(auth, db)


@router.post("/import/{company_id}")
def upload(company_id: int, file: UploadFile = File(...), db: Session = Depends(get_db), auth: AuthJWT = Depends()):
    return handlers.get_xls_handler(file, db, company_id, auth)


@router.post('/get_report')
def get_all_hashrates(year: int = Body(...),
                      file_format: str = Body('json'),
                      company_id: list[int] = Body(None),
                      from_date: date = Body(None),
                      to_date: date = Body(None),
                      auth: AuthJWT = Depends(),
                      db: Session = Depends(get_db)):
    return handlers.get_report_handler(file_format, company_id, from_date, to_date, auth, year, db)


@router.post('/{report_type}')
def get_report_by_type(report_type: str, year: int = Body(...), month: int = Body(...), db: Session = Depends(get_db)):
    return handlers.get_report_by_type_handler(report_type, year, month, db)



