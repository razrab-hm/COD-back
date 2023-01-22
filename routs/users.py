from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from db.base import get_db
from db.schemas import users as dto_users
from _utils import utils
from _utils import handlers

router = APIRouter(prefix='/user')


@router.post('/create', response_model=dto_users.User)
def register_user(user: dto_users.UserCreate, db: Session = Depends(get_db), auth: AuthJWT = Depends()):
    return handlers.create_user_handler(auth, user, db)


@router.post('/create_superuser')
def create_super_user(user: dto_users.UserBase, db: Session = Depends(get_db)):
    return utils.create_super_user(db, user.email, user.password)


@router.post('/login', response_model=dto_users.Token)
def login_user(user: dto_users.UserBase, db: Session = Depends(get_db), auth: AuthJWT = Depends()):
    return handlers.login_user_handler(db, user, auth)


@router.put('/update', response_model=dto_users.User)
def update_user(update_data: dto_users.UserUpdate, db: Session = Depends(get_db), auth: AuthJWT = Depends()):
    return handlers.update_user_handler(update_data, db, auth)


@router.get('/get')
def user(auth: AuthJWT = Depends(), db: Session = Depends(get_db)):
    return handlers.get_user_handler(db, auth)


@router.get('/get_all')
def user(auth: AuthJWT = Depends(), db: Session = Depends(get_db)):
    return handlers.get_all_user_handler(db, auth)


@router.delete('/block')
def user(user_id: int, auth: AuthJWT = Depends(), db: Session = Depends(get_db)):
    return handlers.block_user_handler(db, auth, user_id)



