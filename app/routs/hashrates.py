from datetime import date

from fastapi import APIRouter, Depends, UploadFile, File, Body, Query
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from app.app import handlers
from app.models.schemas import hashrates
from app.app.db import get_db
from app.models.dto import hashrates as dto_hashrates

router = APIRouter(prefix='/hashrates', tags=["hashrates"])


@router.post('/', status_code=201)
def create_hashrate(hashrate: dto_hashrates.HashrateBase, db: Session = Depends(get_db), auth: AuthJWT = Depends()):
    return handlers.create_hashrate_handler(auth, hashrate, db)


@router.get('/', response_model=list[hashrates.HashrateCreate])
def get_all_hashrates(db: Session = Depends(get_db), auth: AuthJWT = Depends()):
    return handlers.get_all_hashrates_handler(db, auth)


@router.get('/company/{company_id}', response_model=list[hashrates.HashrateCreate])
def get_company_hashrates(company_id: int,
                          from_date: date = Query(default=None),
                          to_date: date = Query(default=None),
                          db: Session = Depends(get_db),
                          auth: AuthJWT = Depends()):
    return handlers.get_company_hashrate_handler(company_id, db, auth, from_date, to_date)


@router.put('/')
def update_hashrate(data: dto_hashrates.HashrateUpdate,
                    db: Session = Depends(get_db),
                    auth: AuthJWT = Depends()):
    return handlers.update_hashrate_handler(data, db, auth)


@router.get('/me', response_model=list[hashrates.HashrateCreate])
def get_my_hashrates(auth: AuthJWT = Depends(), db: Session = Depends(get_db)):
    return handlers.get_my_hashrates_handler(auth, db)


@router.post("/import/{company_id}", response_model=list)
def upload(company_id: int, file: UploadFile = File(...), db: Session = Depends(get_db), auth: AuthJWT = Depends()):
    return handlers.get_xls_handler(file, db, company_id, auth)


@router.post("/import/{company_id}/save", response_model=list)
def save_upload(company_id: int, hashrate_list: list = Body(...), auth: AuthJWT = Depends(), db: Session = Depends(get_db)):
    return handlers.save_upload(company_id, hashrate_list, auth, db)


@router.delete('/company/{company_id}')
def delete_hashrates_by_dates(company_id: int,
                              from_date: date = Body(...),
                              to_date: date = Body(...),
                              db: Session = Depends(get_db),
                              auth: AuthJWT = Depends()):
    return handlers.delete_hashrates_by_dates_handler(company_id, db, auth, from_date, to_date)

