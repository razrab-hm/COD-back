import datetime

import openpyxl
import pandas as pd
from fastapi import HTTPException
from openpyxl.worksheet.worksheet import Worksheet
from pandas import Series
from sqlalchemy import extract
from sqlalchemy.orm import Session
from roman import toRoman

from app import json_worker, xls_worker, pdf_worker
from app.db import engine
from models.db import hashrates as db_hashrates


def check_report_type(date_type: str):
    if date_type not in ['year_by_quarters', 'year_by_months', 'year_by_days',
                         'quarter_by_months', 'quarter_by_days', 'month_by_days']:
        raise HTTPException(status_code=404, detail="Date_type format failed")


def month_day_report(db, year, month, output):
    statement = db.query(db_hashrates.Hashrate).filter(extract('year', db_hashrates.Hashrate.date) == year).statement
    dataset = pd.read_sql(statement, engine)

    if len(dataset) < 365:
        base = datetime.datetime(year=year, day=1, month=1)
        date_list = [(base + datetime.timedelta(days=x)).date() for x in range(365)]

        for date in date_list:
            if date not in dataset.date.values:
                dataset = dataset.append({'date': date}, ignore_index=True)

    dataset = dataset.fillna(0)

    dataset['date'] = pd.to_datetime(dataset.date, format='%Y-%m-%d')

    dataset = dataset.sort_values(by='date')

    dataset['month'] = dataset.date.dt.month

    dataset = dataset.loc[dataset.month == month]

    dataset['day']: Series = dataset.date.dt.day
    dataset['month_name']: Series = dataset.date.dt.month_name()

    if output == 'xlsx':
        return xls_worker.month_day_report(dataset, year)
    elif output == 'pdf':
        return pdf_worker.month_day_report(dataset, year)
    else:
        return json_worker.month_day_report(dataset, year)


def year_quarter_month_report(db, year, output):
    statement = db.query(db_hashrates.Hashrate).filter(extract('year', db_hashrates.Hashrate.date) == year).statement
    dataset = pd.read_sql(statement, engine)

    if len(dataset) < 365:
        base = datetime.datetime(year=year, day=1, month=1)
        date_list = [(base + datetime.timedelta(days=x)).date() for x in range(365)]

        for date in date_list:
            if date not in dataset.date.values:
                dataset = dataset.append({'date': date}, ignore_index=True)

    dataset = dataset.fillna(0)

    dataset['date'] = pd.to_datetime(dataset.date, format='%Y-%m-%d')

    dataset = dataset.sort_values(by='date')

    dataset['month_name']: Series = dataset.date.dt.month_name()
    dataset['month']: Series = dataset.date.dt.month
    dataset['quarter']: Series = dataset.date.dt.quarter

    quarter_groups = dataset.groupby('quarter')

    quarter_sum = quarter_groups.hash.sum()

    months_sum: Series = dataset.groupby('month_name').hash.sum()

    if output == 'xlsx':
        return xls_worker.year_quarter_month_report(dataset, quarter_groups, months_sum, quarter_sum)
    elif output == 'pdf':
        return pdf_worker.year_quarter_month_report(dataset, quarter_groups, months_sum, quarter_sum)
    else:
        return json_worker.year_quarter_month_report(dataset, quarter_groups, months_sum, quarter_sum)


def year_quarter_report(db, year):
    statement = db.query(db_hashrates.Hashrate).filter(extract('year', db_hashrates.Hashrate.date) == year).statement
    dataset = pd.read_sql(statement, engine)

    if len(dataset) < 365:
        base = datetime.datetime(year=year, day=1, month=1)
        date_list = [(base + datetime.timedelta(days=x)).date() for x in range(365)]

        for date in date_list:
            if date not in dataset.date.values:
                dataset = dataset.append({'date': date}, ignore_index=True)

    dataset = dataset.fillna(0)

    dataset['date'] = pd.to_datetime(dataset.date, format='%Y-%m-%d')

    dataset = dataset.sort_values(by='date')

    dataset['quarter']: Series = dataset.date.dt.quarter
    quarters_sum: Series = dataset.groupby('quarter').hash.sum()


def year_quarter_month_day_report(db, year):
    statement = db.query(db_hashrates.Hashrate).filter(extract('year', db_hashrates.Hashrate.date) == year).statement
    dataset = pd.read_sql(statement, engine)

    if len(dataset) < 365:
        base = datetime.datetime(year=year, day=1, month=1)
        date_list = [(base + datetime.timedelta(days=x)).date() for x in range(365)]

        for date in date_list:
            if date not in dataset.date.values:
                dataset = dataset.append({'date': date}, ignore_index=True)

    dataset = dataset.fillna(0)

    dataset['date'] = pd.to_datetime(dataset.date, format='%Y-%m-%d')

    dataset = dataset.sort_values(by='date')

    dataset['day']: Series = dataset.date.dt.day
    dataset['month_name']: Series = dataset.date.dt.month_name()
    dataset['month']: Series = dataset.date.dt.month
    dataset['quarter']: Series = dataset.date.dt.quarter

    quarter_groups = dataset.groupby('quarter')

    quarter_sum: Series = quarter_groups.hash.sum()
    #
    months_sum: Series = dataset.groupby('month_name').hash.sum()


def quarter_month_report(db, year, quarter):
    statement = db.query(db_hashrates.Hashrate).filter(extract('year', db_hashrates.Hashrate.date) == year).statement
    dataset = pd.read_sql(statement, engine)

    if len(dataset) < 365:
        base = datetime.datetime(year=year, day=1, month=1)
        date_list = [(base + datetime.timedelta(days=x)).date() for x in range(365)]

        for date in date_list:
            if date not in dataset.date.values:
                dataset = dataset.append({'date': date}, ignore_index=True)

    dataset = dataset.fillna(0)

    dataset['date'] = pd.to_datetime(dataset.date, format='%Y-%m-%d')

    dataset = dataset.sort_values(by='date')

    dataset['quarter']: Series = dataset.date.dt.quarter
    dataset = dataset.loc[dataset.quarter == quarter]

    dataset['month']: Series = dataset.date.dt.month
    dataset['month_name']: Series = dataset.date.dt.month_name()

    month_names = dataset.month_name.unique()
    month_sums = dataset.groupby('month').hash.sum()


def quarter_month_day_report(db, year, quarter):
    statement = db.query(db_hashrates.Hashrate).filter(extract('year', db_hashrates.Hashrate.date) == year).statement
    dataset = pd.read_sql(statement, engine)

    if len(dataset) < 365:
        base = datetime.datetime(year=year, day=1, month=1)
        date_list = [(base + datetime.timedelta(days=x)).date() for x in range(365)]

        for date in date_list:
            if date not in dataset.date.values:
                dataset = dataset.append({'date': date}, ignore_index=True)

    dataset = dataset.fillna(0)

    dataset['date'] = pd.to_datetime(dataset.date, format='%Y-%m-%d')

    dataset = dataset.sort_values(by='date')

    dataset['quarter']: Series = dataset.date.dt.quarter
    dataset['day']: Series = dataset.date.dt.day
    dataset = dataset.loc[dataset.quarter == quarter]

    dataset['month']: Series = dataset.date.dt.month
    dataset['month_name']: Series = dataset.date.dt.month_name()

    months_sum = dataset.groupby('month_name').hash.sum()

