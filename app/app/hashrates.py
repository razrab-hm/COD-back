import pandas as pd
from sqlalchemy.orm import Session

from app.app.db import engine
from app.app.logger import log
from app.models.db import hashrates as db_hashrates
from app.models.db import users as db_users
from app.models.dto import hashrates as dto_hashrates
from app.app import xls_worker


def create_hashrate(db: Session, hashrate: dto_hashrates.HashrateBase):
    log.input(db, hashrate)
    db_hash = db_hashrates.Hashrate(date=hashrate.date, average=hashrate.average, hash=hashrate.hash, company_id=hashrate.company_id)
    db.add(db_hash)
    db.commit()
    db.refresh(db_hash)
    log.output(db_hash)
    return db_hash


def get_hashrate_by_company_id(db: Session, company_id: int, access_level):
    log.input(db, company_id, access_level)
    if access_level == 1:
        return db.query(db_hashrates.Hashrate).filter(db_hashrates.Hashrate.company_id == company_id).all()
    else:
        db.query(db_users.UserCompany).filter()
        return db.query(db_hashrates.Hashrate).join(db_users.UserCompany).filter(db_users.UserCompany.company_id == company_id).all()


def get_data_from_file(file, db, company_id):
    log.input(file)
    data = xls_worker.get_xls_data(file)
    hashrate_list = []
    for date, average in data:
        hashrate_object = {}
        try:
            average = round(float(str(average).replace(',', '.')), 3)
        except:
            average = round(float(str(average.replace(',', '.')[:-1])))

        db_hashrate = db.query(db_hashrates.Hashrate).filter(db_hashrates.Hashrate.date == date).filter(db_hashrates.Hashrate.company_id == company_id).first()
        if db_hashrate:
            hashrate_object['current'] = db_hashrate['average']

        hashrate_object['new'] = average
        hashrate_object['date'] = date
        # hashrate = round(average * 86400 / 1000, 2)
        hashrate_list.append(hashrate_object)

    return hashrate_list


def upload_data(hashrate_list, db, user_id, company_id):
    log.input(hashrate_list, db, user_id, company_id)
    output_info = []
    for date, average, hashrate in hashrate_list:
        db_hashrate = db.query(db_hashrates.Hashrate).filter(db_hashrates.Hashrate.date == date).filter(db_hashrates.Hashrate.company_id == company_id).first()
        if not db_hashrate:
            to_db_hashrate = db_hashrates.Hashrate(date=date, average=average, hash=hashrate, company_id=company_id, user_id=user_id)
            to_output_hashrate = to_db_hashrate.__dict__
            to_output_hashrate['status'] = 'new'
            output_info.append(to_output_hashrate)
            db.add(to_db_hashrate)
        else:
            db_hashrate.average = average
            db_hashrate.hash = hashrate
            db_hashrate.user_id = user_id
            to_output_hashrate = db_hashrate.__dict__
            to_output_hashrate['status'] = 'updated'
            output_info.append(to_output_hashrate)

        db.commit()

    log.output(output_info)
    return output_info


def get_hashrate_by_user_id(db, user_id):
    log.input(db, user_id)
    companies_id = db.query(db_users.UserCompany.company_id).filter(db_users.UserCompany.user_id == user_id)
    hashrates = []
    for company_id in companies_id:
        hashrates.extend(db.query(db_hashrates.Hashrate).filter(db_hashrates.Hashrate.company_id == company_id[0]))
    log.output(hashrates)
    return hashrates


def get_all_hashrates(db):
    return db.query(db_hashrates.Hashrate).all()


def get_dates(db: Session):
    statement = db.query(db_hashrates.Hashrate.date).statement
    dataset = pd.read_sql(statement, engine)

    dataset['date'] = pd.to_datetime(dataset.date, format='%Y-%m-%d')

    dataset = dataset.sort_values(by='date')

    dataset['year'] = dataset.date.dt.year
    dataset['quarter'] = dataset.date.dt.quarter
    dataset['month_name'] = dataset.date.dt.month_name()

    years = [int(year) for year in dataset.year.unique()]
    # quarters = [int(quarter) for quarter in dataset.quarter.unique()]
    # months = [month_name for month_name in dataset.month_name.unique()]

    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    quarters = [1, 2, 3, 4]
    min_year = sorted(years)[0]
    max_year = sorted(years)[-1]
    years = [min_year]
    for i in range(1, max_year - min_year):
        years.append(min_year+i)

    if max_year not in years:
        years.append(max_year)

    return {'years': years, 'quarters': quarters, 'months': months}

