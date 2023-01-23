import hashlib

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.users import get_user_by_email
from db.models import token as db_token


def check_email_in_base(db, email, login=False):
    user = get_user_by_email(db, email)
    if not login:
        if user:
            raise HTTPException(status_code=400, detail="Email already registered")
    else:
        if not user:
            raise HTTPException(status_code=400, detail='Account does`t exists')
        return user


def check_email_valid(email):
    email = email.split('@')
    if len(email) != 2:
        raise HTTPException(status_code=403, detail="Email is not valid")
    _, host = email
    host = host.split('.')
    if len(host) != 2:
        raise HTTPException(status_code=403, detail="Email is not valid")


def check_user_password(password, hash_password):
    if not hashlib.md5(password.encode('utf-8')).hexdigest() == hash_password:
        raise HTTPException(status_code=400, detail="Password incorrect")


def create_tokens(auth, user):
    access_token = auth.create_access_token(subject=user.id)
    refresh_token = auth.create_refresh_token(subject=user.id)
    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }


def add_token_to_blacklist(db: Session, jti: str):
    token = db_token.Token(refresh_token=jti)
    db.add(token)
    db.commit()
    db.refresh(token)
    return db_token


def check_refresh_token_is_in_blacklist(db, auth):
    jti = auth.get_raw_jwt()['jti']
    token_in_blacklist = db.query(db_token.Token).filter(db_token.Token.refresh_token == jti).first()
    if token_in_blacklist:
        raise HTTPException(status_code=400, detail="Refresh token is inactive. Please login again")
