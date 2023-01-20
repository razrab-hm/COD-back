from sqlalchemy.orm import Session

from services.permissions import schemas, models


def create_permission(db: Session, permission: schemas.PermissionBase):
    db_permission = models.Permission(permission_name=permission.permission_name)
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    return db_permission


def get_permission_name(db: Session, permission_id):
    return db.query(models.Permission).filter(models.Permission.id == permission_id).first()

