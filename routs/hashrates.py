from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Body
from fastapi_jwt_auth import AuthJWT
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


@router.post('/year_by_quarters')
def get_all_format_hashrates(company_id=Body(None),
                             from_date=Body(None),
                             to_date=Body(None),
                             auth: AuthJWT = Depends(),
                             db: Session = Depends(get_db)):
    return handlers.get_all_format_hashrates_handler('year_by_quarters', company_id, from_date, to_date, auth, db)


@router.post('/year_by_months')
def get_all_format_hashrates(company_id=Body(...),
                             from_date=Body(...),
                             to_date=Body(...),
                             auth: AuthJWT = Depends(),
                             db: Session = Depends(get_db)):
    return handlers.get_all_format_hashrates_handler('year_by_months', company_id, from_date, to_date, auth, db)


@router.post('/year_by_days')
def get_all_format_hashrates(company_id=Body(...),
                             from_date=Body(...),
                             to_date=Body(...),
                             auth: AuthJWT = Depends(),
                             db: Session = Depends(get_db)):
    return handlers.get_all_format_hashrates_handler('year_by_days', company_id, from_date, to_date, auth, db)


@router.post('/quarter_by_months')
def get_all_format_hashrates(company_id=Body(...),
                             from_date=Body(...),
                             to_date=Body(...),
                             auth: AuthJWT = Depends(),
                             db: Session = Depends(get_db)):
    return handlers.get_all_format_hashrates_handler('quarter_by_months', company_id, from_date, to_date, auth, db)


@router.post('/quarter_by_days')
def get_all_format_hashrates(company_id=Body(...),
                             from_date=Body(...),
                             to_date=Body(...),
                             auth: AuthJWT = Depends(),
                             db: Session = Depends(get_db)):
    return handlers.get_all_format_hashrates_handler('quarter_by_days', company_id, from_date, to_date, auth, db)


@router.post('/month_by_days')
def get_all_format_hashrates(company_id=Body(...),
                             from_date=Body(...),
                             to_date=Body(...),
                             auth: AuthJWT = Depends(),
                             db: Session = Depends(get_db)):
    return handlers.get_all_format_hashrates_handler('month_by_days', company_id, from_date, to_date, auth, db)


