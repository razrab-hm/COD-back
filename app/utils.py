from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from db.schemas import (hashrates as dto_hashrates,
                        users as dto_users)
from db.models import (hashrates as db_hashrates)


def create_hash(db: Session, hashrate: dto_hashrates.HashrateBase):
    db_hash = db_hashrates.Hashrate(date=hashrate.date, average=hashrate.average, hash=hashrate.hash, company_id=hashrate.company_id)
    db.add(db_hash)
    db.commit()
    db.refresh(db_hash)
    return db_hash


def get_hash_by_company_id(db: Session, id: int):
    return db.query(db_hashrates.Hashrate).filter(db_hashrates.Hashrate.company_id == id).all()


@AuthJWT.load_config
def get_config():
    return dto_users.Settings()

