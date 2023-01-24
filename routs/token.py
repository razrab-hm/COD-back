from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from app.db import get_db
from app import handlers

router = APIRouter(prefix='/token')


@router.post('/refresh')
def refresh(auth: AuthJWT = Depends(), db: Session = Depends(get_db)):
    return handlers.refresh_handler(auth, db)

