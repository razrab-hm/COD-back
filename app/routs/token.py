from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from app.app.db import get_db
from app.app import handlers

router = APIRouter(prefix='/tokens', tags=["tokens"])


@router.post('/refresh')
def refresh(auth: AuthJWT = Depends(), db: Session = Depends(get_db)):
    return handlers.refresh_handler(auth, db)


@router.get('/')
def check_token(auth: AuthJWT = Depends(), db: Session = Depends(get_db)):
    return handlers.check_token_valid(db, auth)



