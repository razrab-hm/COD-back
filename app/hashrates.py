import numpy
import pandas as pd
from fastapi import HTTPException
from pandas import Series
from pandas.core.groupby import DataFrameGroupBy
from sqlalchemy import extract
from sqlalchemy.orm import Session

from models.db import hashrates as db_hashrates, users as db_users
from models.dto import hashrates as dto_hashrates
from app import xls_worker
from app.db import engine


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


def check_report_type(date_type: str):
    if date_type not in ['year_by_quarters', 'year_by_months', 'year_by_days',
                         'quarter_by_months', 'quarter_by_days', 'month_by_days']:
        raise HTTPException(status_code=404, detail="Date_type format failed")


def get_by_type(db: Session, report_type, year):
    statement = db.query(db_hashrates.Hashrate).filter(extract('year', db_hashrates.Hashrate.date) == 2022).statement

    dataset = pd.read_sql(statement, engine)
    dataset['date'] = pd.to_datetime(dataset.date, format='%Y-%m-%d')

    dataset['day'] = dataset.date.dt.day
    dataset['month']: Series = dataset.date.dt.month
    dataset['quarter'] = dataset.date.dt.quarter

    months_sum: Series = dataset.groupby('month').hash.sum()
    months_sum = months_sum.add_suffix('-month')
    # print(months_sum)

    test = {
        'year': {'1-quarter': {
            '1-month': {
                '1-day': {'total': 0},
                'total': 0
            }, 'total': 0
        }, 'total': 0}
    }

    quarters_sum: Series = dataset.groupby('quarter').hash.sum()
    quarters_sum = quarters_sum.add_suffix('-quarter')

    year_sum = quarters_sum.sum()
    report = {'year': {}}
    # for name, val in quarters_sum.to_dict().items():
    #     report['year'].update({name: {'total': val}})

    for quarter in dataset.quarter.unique():
        report['year'][f'{quarter}-quarter'] = {'total': 0}
        for month in dataset.loc[dataset.quarter == quarter].month.unique():
            report['year'][f'{quarter}-quarter'][f'{month}-month'] = {'total': 0}
            for day in dataset.loc[dataset.month == month].day:
                report['year'][f'{quarter}-quarter'][f'{month}-month'][f'{day}-day'] = {'total': 0}

    # for name, val in months_sum

    # print(type(quarters_sum))
    # report = {f'quarter-{quarter_id}': quarter_value for quarter_id, quarter_value in quarters_sum}

    return report
