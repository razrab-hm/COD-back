from fastapi import APIRouter, Depends, Body
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from app.app import handlers
from app.app.db import get_db

router = APIRouter(prefix='/reports', tags=["reports"])


@router.post('/month_day')
def month_day(output_type: str = Body(...),
                       year: int = Body(...),
                       month: int = Body(...),
                       db: Session = Depends(get_db),
                       auth: AuthJWT = Depends()):
    return handlers.month_day_report_handler(output_type, year, month, db, auth)


@router.post('/year_quarter_month')
def year_quarter_month(output_type: str = Body(...),
                       year: int = Body(...),
                       db: Session = Depends(get_db),
                       auth: AuthJWT = Depends()):
    return handlers.year_quarter_month_report_handler(output_type, year, db, auth)


@router.post('/year_quarter')
def year_quarter(output_type: str = Body(...),
                 year: int = Body(...),
                 db: Session = Depends(get_db),
                 auth: AuthJWT = Depends()):
    return handlers.year_quarter_report_handler(output_type, year, db, auth)


@router.post('/year_quarter_month_day')
def year_quarter_month_day(output_type: str = Body(...),
                           year: int = Body(...),
                           db: Session = Depends(get_db),
                           auth: AuthJWT = Depends()):
    return handlers.year_quarter_month_day_report_handler(output_type, year, db, auth)


@router.post('/quarter_month')
def quarter_month(output_type: str = Body(...),
                  year: int = Body(...),
                  quarter: int = Body(...),
                  db: Session = Depends(get_db),
                  auth: AuthJWT = Depends()):
    return handlers.quarter_month_report_handler(output_type, year, quarter, db, auth)


@router.post('/quarter_month_day')
def quarter_month_day(output_type: str = Body(...),
                  year: int = Body(...),
                  quarter: int = Body(...),
                  db: Session = Depends(get_db),
                  auth: AuthJWT = Depends()):
    return handlers.quarter_month_day_report_handler(output_type, year, quarter, db, auth)


@router.get('/dates')
def get_dates(auth: AuthJWT = Depends(), db: Session = Depends(get_db)):
    return handlers.get_dates_handler(auth, db)

