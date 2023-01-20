from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from db.base import get_db
from utils import utils as base
from db.schemas import permissions as dto_permissions

router = APIRouter(prefix='/permission')


@router.post('/create', response_model=dto_permissions.Permission)
def create_permission(permission: dto_permissions.PermissionBase, db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    authorize.jwt_required()

    current_user = authorize.get_jwt_subject()
    user_permission = base.get_user_by_id(db, current_user).permission_id

    if not user_permission < 3:
        raise HTTPException(status_code=401, detail="You don't have permissions")

    data = base.create_permission(db, permission)
    return data


@router.get('/get')
def get_my_permissions(authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    authorize.jwt_required()

    current_user = authorize.get_jwt_subject()
    user = base.get_user_by_id(db, current_user)
    role = base.get_permission_name(db, user.permission_id)
    return {'role': role}


