from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from users import schemas, base
from users.base import get_db

router = APIRouter(prefix='/user')


@router.post('/register', response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = base.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    data = base.create_user(db=db, user=user)
    return data


@router.post('/login', response_model=schemas.TokenBase)
def login_user(user: schemas.UserBase, db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    db_user = base.get_user_by_email(db, email=user.email)
    if not db_user:
        raise HTTPException(status_code=401, detail="Email not registred!")
    if not user.password + 'notreallyhashed' == db_user.hash_password:
        raise HTTPException(status_code=401, detail="Password incorrect!")
    access_token = authorize.create_access_token(subject=user.email, expires_time=900)
    refresh_token = authorize.create_refresh_token(subject=user.email)
    return {"access_token": access_token, "refresh_token": refresh_token}


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
def user(authorize: AuthJWT = Depends()):
    authorize.jwt_required()

    current_user = authorize.get_jwt_subject()
    return {"user": current_user}

