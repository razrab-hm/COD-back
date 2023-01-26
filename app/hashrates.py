from sqlalchemy.orm import Session

from app.reports import month_day_report
from models.db import hashrates as db_hashrates, users as db_users
from models.dto import hashrates as dto_hashrates
from app import xls_worker


def create_hashrate(db: Session, hashrate: dto_hashrates.HashrateBase):
    db_hash = db_hashrates.Hashrate(date=hashrate.date, average=hashrate.average, hash=hashrate.hash, company_id=hashrate.company_id)
    db.add(db_hash)
    db.commit()
    db.refresh(db_hash)
    return db_hash


def get_hashrate_by_company_id(db: Session, company_id: int, access_level, from_user_id):
    if access_level == 1:
        return db.query(db_hashrates.Hashrate).filter(db_hashrates.Hashrate.company_id == company_id).all()
    else:
        db.query(db_users.UserCompany).filter()
        return db.query(db_hashrates.Hashrate).join(db_users.UserCompany).filter(db_users.UserCompany.company_id == company_id).all()


def get_data_from_file(file, db, company_id, user_id):
    data = xls_worker.get_xls_data(file)
    hashrate_list = []
    for date, hashrate in data:
        db_hashrate = db.query(db_hashrates.Hashrate).filter(db_hashrates.Hashrate.date == date).filter(db_hashrates.Hashrate.company_id == company_id).first()
        if not db_hashrate:
            to_db_hashrate = db_hashrates.Hashrate(date=date, average=round(hashrate/86400*1000, 2), hash=hashrate, company_id=company_id, user_id=user_id)
            to_output_hashrate = to_db_hashrate.__dict__
            to_output_hashrate['status'] = 'new'
            hashrate_list.append(to_output_hashrate)
            db.add(to_db_hashrate)
        else:
            db_hashrate.average = round(hashrate/86400*1000, 2)
            db_hashrate.hash = hashrate
            db_hashrate.user_id = user_id
            to_output_hashrate = db_hashrate.__dict__
            to_output_hashrate['status'] = 'updated'
            hashrate_list.append(to_output_hashrate)

        db.commit()
    return hashrate_list


def get_hashrate_by_user_id(db, user_id):
    companies_id = db.query(db_users.UserCompany.company_id).filter(db_users.UserCompany.user_id == user_id)
    hashrates = []
    for company_id in companies_id:
        hashrates.extend(db.query(db_hashrates.Hashrate).filter(db_hashrates.Hashrate.company_id == company_id[0]))
    return hashrates


def get_all_hashrates(db):
    return db.query(db_hashrates.Hashrate).all()



