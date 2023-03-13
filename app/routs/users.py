from fastapi import APIRouter, Depends, Body, Query
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from app.app.db import get_db
from app.models.schemas import users
from app.models.dto import users as dto_users
from app.app import handlers

router = APIRouter(prefix='/users', tags=["users"])


@router.post('/', status_code=201, response_model=users.UserRegister)
def register_user(user: dto_users.UserCreate, db: Session = Depends(get_db), auth: AuthJWT = Depends()):
    return handlers.create_user_handler(auth, user, db)


@router.post('/new')
def new_user(user: dto_users.UserCreateAdmin, db: Session = Depends(get_db), auth: AuthJWT = Depends()):
    return handlers.new_user_handler(user, db, auth)


@router.post('/login', status_code=202)
def login_user(user: dto_users.UserBase, db: Session = Depends(get_db), auth: AuthJWT = Depends()):
    return handlers.login_user_handler(db, user, auth)


@router.post('/logout', status_code=205, response_model=users.UserLogout)
def logout_user(db: Session = Depends(get_db), auth: AuthJWT = Depends()):
    return handlers.logout_handler(db, auth)


# @router.get('/inactive', response_model=)
# def check_inactive(db: Session = Depends(get_db), auth: AuthJWT = Depends()):
#     handlers.get_inactive(db, auth)


@router.put('/', response_model=users.UserUpdate)
def update_user(update_data: dto_users.UserUpdate, db: Session = Depends(get_db), auth: AuthJWT = Depends()):
    user = handlers.update_user_handler(update_data, db, auth)
    return user


@router.get('/me', status_code=200, response_model=users.UserMe)
def get_user(auth: AuthJWT = Depends(), db: Session = Depends(get_db)):
    return handlers.get_user_handler(db, auth)


@router.get('/', status_code=200, response_model=list[users.UserGetId])
def get_all_users(role: str = Query(default='all'),
                  companies_id: list[int] = Query(default=[0]),
                  inactive: bool = Query(default=False),
                  auth: AuthJWT = Depends(),
                  db: Session = Depends(get_db)):
    return handlers.get_all_users_handler(db, auth, role, companies_id, inactive)


@router.get('/{user_id}', response_model=users.UserGetId)
def get_user_by_id(user_id: int, auth: AuthJWT = Depends(), db: Session = Depends(get_db)):
    return handlers.get_user_by_id_handler(db, user_id, auth)


@router.delete('/{user_id}', status_code=202, response_model=users.UserGetId)
def set_inactive_user(user_id: int, auth: AuthJWT = Depends(), db: Session = Depends(get_db)):
    return handlers.set_inactive_user(db, auth, user_id)


@router.get('/companies/{company_id}', response_model=list[users.UserGetId])
def get_company_users(company_id: int, auth: AuthJWT = Depends(), db: Session = Depends(get_db)):
    user = handlers.get_company_users_handler(db, company_id, auth)
    return user


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


@router.put('/update_companies', response_model=users.UserUpdateCompanies)
def update_user_companies(user_id: int = Body(...),
                          companies_id: list[int] = Body(...),
                          auth: AuthJWT = Depends(),
                          db: Session = Depends(get_db)):
    return handlers.update_user_companies_handler(user_id, companies_id, auth, db)



