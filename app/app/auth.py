import hashlib

from fastapi import HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from app.app.users import get_user_by_username, get_user_by_email
from app.models.db import auth as db_token
from app.models.db import users as db_users
from app.models.dto import users as dto_users


def check_username_in_base(db, username, login=False):
    user = get_user_by_username(db, username)
    if not login:
        if user:
            raise HTTPException(status_code=406, detail="Username already registered")
    else:
        if not user:
            raise HTTPException(status_code=401, detail='Username or password incorrect')
        return user


def check_email_in_base(db, email, login=False):
    user = get_user_by_email(db, email)
    if not login:
        if user:
            raise HTTPException(status_code=406, detail="Email already registered")
    else:
        if not user:
            raise HTTPException(status_code=401, detail='Username or password incorrect')
        return user


def check_inactive_account(db, user_id):
    inactive = db.query(db_users.User.inactive).filter(db_users.User.id == user_id).first()
    if inactive.inactive:
        raise HTTPException(status_code=401, detail="Inactive account!")


def check_email_valid(email):
    email = email.split('@')
    if len(email) != 2:
        raise HTTPException(status_code=406, detail="Email is not valid")
    _, host = email
    host = host.split('.')
    if len(host) != 2:
        raise HTTPException(status_code=406, detail="Email is not valid")


def check_user_password(password, hash_password):
    if not hashlib.md5(password.encode('utf-8')).hexdigest() == hash_password:
        raise HTTPException(status_code=401, detail="Username or password incorrect")


def create_tokens(auth, user_id, role=None):
    access_token = auth.create_access_token(subject=user_id, expires_time=60*25)
    refresh_token = auth.create_refresh_token(subject=user_id)
    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'role': role
    }


def add_token_to_blacklist(db: Session, jti: str):
    token = db_token.Token(refresh_token=jti)
    db.add(token)
    db.commit()
    db.refresh(token)
    return db_token


def check_refresh_token_is_in_blacklist(db, jti):
    token_in_blacklist = db.query(db_token.Token).filter(db_token.Token.refresh_token == jti).first()
    if token_in_blacklist:
        raise HTTPException(status_code=401, detail="Refresh token is inactive. Please login again")


@AuthJWT.load_config
def get_config():
    return dto_users.Settings()
