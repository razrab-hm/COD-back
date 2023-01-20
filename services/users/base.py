from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from services.users import schemas, models
from services.companies import models as company_models


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_id(db: Session, id: int):
    return db.query(models.User).filter(models.User.id == id).first()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hash_password=fake_hashed_password, permission_id=user.permission_id, company_id=user.company_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def set_user_company(db: Session, email: str, company_id: int):
    req = db.query(models.User).filter(models.User.email == email).update({'company_id': company_id})
    db.commit()
    return req


@AuthJWT.load_config
def get_config():
    return schemas.Settings()



