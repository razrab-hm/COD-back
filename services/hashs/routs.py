from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core.base import get_db
from services.hashs import schemas, base
from services.users import base as user_base
from services.companies import base as company_base

router = APIRouter(prefix='/hash')


@router.post('/create', response_model=schemas.Hash)
def create_hash(hash: schemas.HashBase, db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    current_user = authorize.get_jwt_subject()
    user_permission = user_base.get_user_by_id(db, current_user).permission_id

    if not user_permission < 3:
        raise HTTPException(status_code=401, detail="You don't have permissions")

    data = base.create_hash(db, hash)
    return data


@router.get('/user_hash')
def get_user_hash(db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    authorize.jwt_required()

    current_user = authorize.get_jwt_subject()
    company_id = user_base.get_user_by_id(db, current_user).company_id
    data = base.get_hash_by_company_id(db, company_id)

    return data

