from fastapi import APIRouter, Depends, Body
from fastapi_jwt_auth import AuthJWT
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.app import handlers
from app.app.db import get_db

router = APIRouter(prefix='/reports', tags=["reports"])


@router.post('/month_day')
def month_day(output_type: str = Body(...),
                       year: int = Body(...),
                       month: int = Body(...),
                       companies: list = Body(...),
                       db: Session = Depends(get_db),
                       auth: AuthJWT = Depends()):
    return handlers.month_day_report_handler(output_type, companies, year, month, db, auth)


@router.post('/year_quarter_month')
def year_quarter_month(output_type: str = Body(...),
                       year: int = Body(...),
                       companies: list = Body(...),
                       db: Session = Depends(get_db),
                       auth: AuthJWT = Depends()):
    return handlers.year_quarter_month_report_handler(output_type, companies, year, db, auth)


@router.post('/year_quarter')
def year_quarter(output_type: str = Body(...),
                 year: int = Body(...),
                 companies: list = Body(...),
                 db: Session = Depends(get_db),
                 auth: AuthJWT = Depends()):
    return handlers.year_quarter_report_handler(output_type, companies, year, db, auth)


@router.post('/year_quarter_month_day')
def year_quarter_month_day(output_type: str = Body(...),
                           year: int = Body(...),
                           companies: list = Body(...),
                           db: Session = Depends(get_db),
                           auth: AuthJWT = Depends()):
    return handlers.year_quarter_month_day_report_handler(output_type, companies, year, db, auth)


@router.post('/quarter_month')
def quarter_month(output_type: str = Body(...),
                  year: int = Body(...),
                  quarter: int = Body(...),
                  companies: list = Body(...),
                  db: Session = Depends(get_db),
                  auth: AuthJWT = Depends()):
    return handlers.quarter_month_report_handler(output_type, companies, year, quarter, db, auth)


@router.post('/quarter_month_day')
def quarter_month_day(output_type: str = Body(...),
                  year: int = Body(...),
                  quarter: int = Body(...),
                  companies: list = Body(...),
                  db: Session = Depends(get_db),
                  auth: AuthJWT = Depends()):
    return handlers.quarter_month_day_report_handler(output_type, companies, year, quarter, db, auth)


@router.get('/dates')
def get_dates(auth: AuthJWT = Depends(), db: Session = Depends(get_db)):
    return handlers.get_dates_handler(auth, db)


@router.get('/xlsx')
def get_xlsx():
    return FileResponse('xlsx.xls', media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', headers={'Content-Disposition': 'attachment; filename="Book.xls"'})


