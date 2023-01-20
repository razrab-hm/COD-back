from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from db.base import get_db
from db import schemas
from _utils import utils
from _utils import handlers

router = APIRouter(prefix='/user')


@router.post('/create', response_model=schemas.users.User)
def register_user(user: schemas.users.UserCreate, db: Session = Depends(get_db), auth: AuthJWT = Depends()):
    return handlers.create_user_handler(auth, user, db)


@router.post('/create_superuser')
def create_super_user(user: schemas.users.UserBase, db: Session = Depends(get_db)):
    return utils.create_super_user(db, user.email, user.password)


@router.post('/login', response_model=schemas.users.TokenBase)
def login_user(user: schemas.users.UserBase, db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    db_user = utils.get_user_by_email(db, email=user.email)
    if not db_user:
        raise HTTPException(status_code=401, detail="Email not registred!")
    if not user.password + 'notreallyhashed' == db_user.hash_password:
        raise HTTPException(status_code=401, detail="Password incorrect!")

    access_token = authorize.create_access_token(subject=db_user.id, expires_time=900)
    refresh_token = authorize.create_refresh_token(subject=user.email)
    return {"access_token": access_token, "refresh_token": refresh_token}


@router.put('/update', response_model=schemas.users.User)
def update_user(update_data: schemas.users.UserUpdate, db: Session = Depends(get_db), auth: AuthJWT = Depends()):
    return handlers.update_user_handler(update_data, db, auth)


@router.post('/refresh')
def refresh(authorize: AuthJWT = Depends()):
    """
    The jwt_refresh_token_required() function insures a valid refresh
    token is present in the request before running any code below that function.
    we can use the get_jwt_subject() function to get the subject of the refresh
    token, and use the create_access_token() function again to make a new access token
    """
    authorize.jwt_refresh_token_required()

    current_user = authorize.get_jwt_subject()
    new_access_token = authorize.create_access_token(subject=current_user)
    return {"access_token": new_access_token}


@router.get('/user')
def user(authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    authorize.jwt_required()

    current_user = authorize.get_jwt_subject()
    return {"user": utils.get_user_by_id(db, current_user)}


@router.post('/set_company')
def set_user_company(email: str, company_id: int, authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    authorize.jwt_required()
    print(email)
    current_user = authorize.get_jwt_subject()
    user_permission = utils.get_user_by_id(db, current_user).permission_id

    if not user_permission < 3:
        raise HTTPException(status_code=401, detail="You don't have permissions")

    data = utils.set_user_company(db, email, company_id)
    return data

