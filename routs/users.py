from fastapi import APIRouter, Depends, Body
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

import app.users
from app.db import get_db
from models.dto import users as dto_users
from app import handlers

router = APIRouter(prefix='/users')


@router.post('/', response_model=dto_users.User)
def register_user(user: dto_users.UserCreate, db: Session = Depends(get_db), auth: AuthJWT = Depends()):
    return handlers.create_user_handler(auth, user, db)


@router.post('/create_superuser')
def create_super_user(user: dto_users.UserCreate, db: Session = Depends(get_db)):
    return app.users.create_super_user(db, user.email, user.password)


@router.post('/login', response_model=dto_users.Token)
def login_user(user: dto_users.UserCreate, db: Session = Depends(get_db), auth: AuthJWT = Depends()):
    return handlers.login_user_handler(db, user, auth)


@router.put('/', response_model=dto_users.User)
def update_user(update_data: dto_users.UserUpdate, db: Session = Depends(get_db), auth: AuthJWT = Depends()):
    return handlers.update_user_handler(update_data, db, auth)


@router.get('/me', response_model=dto_users.User)
def get_user(auth: AuthJWT = Depends(), db: Session = Depends(get_db)):
    return handlers.get_user_handler(db, auth)


@router.get('/', response_model=list[dto_users.User])
def get_all_users(auth: AuthJWT = Depends(), db: Session = Depends(get_db)):
    return handlers.get_all_users_handler(db, auth)


@router.get('/{user_id}')
def get_user_by_id(user_id: int, auth: AuthJWT = Depends(), db: Session = Depends(get_db)):
    return handlers.get_user_by_id_handler(db, user_id, auth)


@router.delete('/{user_id}', response_model=dto_users.User)
def set_inactive_user(user_id: int, auth: AuthJWT = Depends(), db: Session = Depends(get_db)):
    return handlers.set_inactive_user(db, auth, user_id)


@router.get('/companies/{company_id}')
def get_company_users(company_id: int, auth: AuthJWT = Depends(), db: Session = Depends(get_db)):
    return handlers.get_company_users_handler(db, company_id, auth)


@router.post('/add_company')
def add_user_company(company_id: int = Body(),
                     user_id: int = Body(),
                     auth: AuthJWT = Depends(),
                     db: Session = Depends(get_db)):
    return handlers.add_company_handler(company_id, user_id, auth, db)


@router.post('/remove_company')
def add_user_company(company_id: int = Body(),
                     user_id: int = Body(),
                     auth: AuthJWT = Depends(),
                     db: Session = Depends(get_db)):
    return handlers.remove_company_handler(company_id, user_id, auth, db)
