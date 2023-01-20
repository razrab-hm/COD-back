from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from db.base import get_db
from utils import utils as base
from db.schemas import hashrates as dto_hashrates

router = APIRouter(prefix='/hashrate')


@router.post('/create', response_model=dto_hashrates.Hashrate)
def create_hash(hashrate: dto_hashrates.HashrateBase, db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    current_user = authorize.get_jwt_subject()
    user_permission = base.get_user_by_id(db, current_user).permission_id
    if not user_permission < 3:
        raise HTTPException(status_code=401, detail="You don't have permissions")

    data = base.create_hash(db, hashrate)
    return data


@router.get('/user_hash')
def get_user_hash(db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    authorize.jwt_required()

    current_user = authorize.get_jwt_subject()
    company_id = base.get_user_by_id(db, current_user).company_id
    data = base.get_hash_by_company_id(db, company_id)

    return data

