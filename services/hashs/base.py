from sqlalchemy.orm import Session

from services.hashs import schemas, models


def create_hash(db: Session, hash: schemas.HashBase):
    db_hash = models.Hash(date=hash.date, average=hash.average, hash=hash.hash, company_id=hash.company_id)
    db.add(db_hash)
    db.commit()
    db.refresh(db_hash)
    return db_hash


def get_hash_by_company_id(db: Session, id: int):
    return db.query(models.Hash).filter(models.Hash.company_id == id).all()

