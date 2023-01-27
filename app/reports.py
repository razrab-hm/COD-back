import datetime

import openpyxl
import pandas as pd
from fastapi import HTTPException
from openpyxl.worksheet.worksheet import Worksheet
from pandas import Series, DataFrame
from pandas.core.groupby import DataFrameGroupBy
from sqlalchemy import extract
from sqlalchemy.orm import Session
from roman import toRoman

from app.db import engine
from models.db import hashrates as db_hashrates


def check_report_type(date_type: str):
    if date_type not in ['year_by_quarters', 'year_by_months', 'year_by_days',
                         'quarter_by_months', 'quarter_by_days', 'month_by_days']:
        raise HTTPException(status_code=404, detail="Date_type format failed")


def get_report(db: Session, file_format, company_id, from_date, to_date, auth, year):
    statement = db.query(db_hashrates.Hashrate).filter(extract('year', db_hashrates.Hashrate.date) == year)
    if company_id:
        statement = statement.filter(db_hashrates.Hashrate.company_id == company_id)
    if from_date:
        statement = statement.filter(db_hashrates.Hashrate.date >= from_date)
    if to_date:
        statement = statement.filter(db_hashrates.Hashrate.date <= to_date)

    statement = statement.statement

    dataset = pd.read_sql(statement, engine)
    dataset['date'] = pd.to_datetime(dataset.date, format='%Y-%m-%d')

    dataset['day'] = dataset.date.dt.day
    dataset['month']: Series = dataset.date.dt.month
    dataset['quarter'] = dataset.date.dt.quarter

    months_sum: Series = dataset.groupby('month').hash.sum()
    quarters_sum: Series = dataset.groupby('quarter').hash.sum()
    year_sum = quarters_sum.sum()

    if file_format == 'excel':
        wb = openpyxl.Workbook()
        ws: Worksheet = wb.active
        row_counter = 1

        ws.column_dimensions['A'].width = 30
        ws.column_dimensions['B'].width = 15

        ws.cell(row=row_counter, column=1, value=f'{year}-year')
        ws.cell(row=row_counter, column=2, value=year_sum)
        row_counter += 1
        for quarter in dataset.quarter.unique():
            ws.cell(row=row_counter, column=1, value=f'{quarter}-quarter')
            ws.cell(row=row_counter, column=2, value=quarters_sum.get(quarter))
            row_counter += 1
            for month in dataset.loc[dataset.quarter == quarter].month.unique():
                ws.cell(row=row_counter, column=1, value=f'{month}-month')
                ws.cell(row=row_counter, column=2, value=months_sum.get(month))
                row_counter += 1
                for day, day_value in dataset.loc[dataset.month == month][['day', 'hash']].values:
                    ws.cell(row=row_counter, column=1, value=f'{int(day)}-day')
                    ws.cell(row=row_counter, column=2, value=day_value)
                    row_counter += 1

        wb.save("sample.xlsx")
        return
    elif file_format == 'pdf':
        pass
    else:
        report = {'year': {'total': year_sum}}
        for quarter in dataset.quarter.unique():
            report['year'][f'{int(quarter)}-quarter'] = {'total': quarters_sum.get(quarter)}
            for month in dataset.loc[dataset.quarter == quarter].month.unique():
                report['year'][f'{int(quarter)}-quarter'][f'{int(month)}-month'] = {'total': months_sum.get(month)}
                for day, day_value in dataset.loc[dataset.month == month][['day', 'hash']].values:
                    report['year'][f'{int(quarter)}-quarter'][f'{int(month)}-month'][f'{int(day)}-day'] = {
                        'total': day_value}

        return report


def month_day_report(db, year, month):
    statement = db.query(db_hashrates.Hashrate).filter(extract('year', db_hashrates.Hashrate.date) == year).statement
    dataset = pd.read_sql(statement, engine)

    if len(dataset) < 365:
        base = datetime.datetime(year=year, day=1, month=1)
        date_list = [(base + datetime.timedelta(days=x)).date() for x in range(365)]

        for date in date_list:
            if date not in dataset.date.values:
                dataset = dataset.append({'date': date}, ignore_index=True)

    dataset['date'] = pd.to_datetime(dataset.date, format='%Y-%m-%d')
    dataset['month'] = dataset.date.dt.month

    dataset = dataset.loc[dataset.month == month]

    dataset['day']: Series = dataset.date.dt.day
    dataset['month_name']: Series = dataset.date.dt.month_name()

    report = []

    for day, hash, average, month_name in dataset[['day', 'hash', 'average', 'month_name']].values:
        report.append({'total': hash, 'average': average, 'date': f'{month_name[0:3]}. {day}, {year}'})

    return {'report': report, 'total': dataset.hash.sum()}


def year_quarter_month_report(db, year):
    statement = db.query(db_hashrates.Hashrate).filter(extract('year', db_hashrates.Hashrate.date) == year).statement
    dataset = pd.read_sql(statement, engine)

    if len(dataset) < 365:
        base = datetime.datetime(year=year, day=1, month=1)
        date_list = [(base + datetime.timedelta(days=x)).date() for x in range(365)]

        for date in date_list:
            if date not in dataset.date.values:
                dataset = dataset.append({'date': date}, ignore_index=True)

    dataset['date'] = pd.to_datetime(dataset.date, format='%Y-%m-%d')
    dataset['month_name']: Series = dataset.date.dt.month_name()
    dataset['month']: Series = dataset.date.dt.month
    dataset['quarter']: Series = dataset.date.dt.quarter

    quarter_groups = dataset.groupby('quarter')

    months_sum: Series = dataset.groupby('month').hash.sum()

    report = {}
    for quarter in quarter_groups:
        month_list = []
        month_groups = zip(quarter[1]['month'].unique(), quarter[1]['month_name'].unique())
        for month, month_name in month_groups:
            month_list.append({'date': year, 'name': month_name, 'total': months_sum.get(month)})
        report.update({f'quarter_{quarter[0]}': month_list})

    return {'report': report, 'total': dataset.hash.sum()}


def year_quarter_report(db, year):
    statement = db.query(db_hashrates.Hashrate).filter(extract('year', db_hashrates.Hashrate.date) == year).statement
    dataset = pd.read_sql(statement, engine)

    if len(dataset) < 365:
        base = datetime.datetime(year=year, day=1, month=1)
        date_list = [(base + datetime.timedelta(days=x)).date() for x in range(365)]

        for date in date_list:
            if date not in dataset.date.values:
                dataset = dataset.append({'date': date}, ignore_index=True)

    dataset['date'] = pd.to_datetime(dataset.date, format='%Y-%m-%d')
    dataset['quarter']: Series = dataset.date.dt.quarter
    quarters_sum: Series = dataset.groupby('quarter').hash.sum()
    report = []

    for quarter_pk, quarter_sum in quarters_sum.items():
        print(quarter_pk, quarter_sum)
        report.append({'total': quarter_sum, 'quarter': quarter_pk})

    return {'report': report, 'total': dataset.hash.sum()}


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

    # quarter_sum: Series = quarter_groups.hash.sum()
    #
    # months_sum: Series = dataset.groupby('month').hash.sum()

    report = []
    # for quarter in quarter_groups:
    #     month_list = []
    #     month_groups = zip(quarter[1]['month'].unique(), quarter[1]['month_name'].unique())
    #     for month, month_name in month_groups:
    #         day_list = []
    #         for day, hash, average in dataset.loc[dataset.month == month][['day', 'hash', 'average']].values:
    #             day_list.append({int(day): {'total': hash, 'average': average, 'date': f'{month_name[0:3]}. {int(day)}, {year}'}})
    #         month_list.append({int(month): day_list, 'date': f'{month_name[0:3]}. {year}', 'total': months_sum.get(month)})
    #     report.update({quarter[0]: month_list, 'total': quarter_sum.get(quarter[0])})
    for quarter in quarter_groups:
        for month_ds in dataset.loc[dataset.quarter == quarter[0]][['month', 'month_name']].values:
            for day_ds in dataset.loc[dataset.month == month_ds[0]][['day', 'hash', 'month_name']].values:
                report.append({'type': 'day', 'date': f'{day_ds[2][0:3]}. {day_ds[0]}', 'hash': day_ds[1]})

            report.append({'type': 'month', 'date': f'{month_ds[1]}'})

        report.append({'type': 'quarter', 'date': f'{toRoman(quarter[0])} quarter'})

    return {'report': report, 'total': dataset.hash.sum()}


def quarter_month_report(db, year, quarter):
    statement = db.query(db_hashrates.Hashrate).filter(extract('year', db_hashrates.Hashrate.date) == year).statement
    dataset = pd.read_sql(statement, engine)

    if len(dataset) < 365:
        base = datetime.datetime(year=year, day=1, month=1)
        date_list = [(base + datetime.timedelta(days=x)).date() for x in range(365)]

        for date in date_list:
            if date not in dataset.date.values:
                dataset = dataset.append({'date': date}, ignore_index=True)

    dataset['date'] = pd.to_datetime(dataset.date, format='%Y-%m-%d')
    dataset['quarter']: Series = dataset.date.dt.quarter
    dataset = dataset.loc[dataset.quarter == quarter]

    dataset['month']: Series = dataset.date.dt.month
    dataset['month_name']: Series = dataset.date.dt.month_name()

    month_names = dataset.month_name.unique()
    month_sums = dataset.groupby('month').hash.sum()

    report = []
    for (month_pk, month_sum), month_name in zip(month_sums.items(), month_names):
        report.append({int(month_pk): {'date': month_name, 'total': month_sum}})

    return {'report': report, 'total': dataset.hash.sum()}


def quarter_month_day_report(db, year, quarter):
    statement = db.query(db_hashrates.Hashrate).filter(extract('year', db_hashrates.Hashrate.date) == year).statement
    dataset = pd.read_sql(statement, engine)

    if len(dataset) < 365:
        base = datetime.datetime(year=year, day=1, month=1)
        date_list = [(base + datetime.timedelta(days=x)).date() for x in range(365)]

        for date in date_list:
            if date not in dataset.date.values:
                dataset = dataset.append({'date': date}, ignore_index=True)

    dataset['date'] = pd.to_datetime(dataset.date, format='%Y-%m-%d')
    dataset['quarter']: Series = dataset.date.dt.quarter
    dataset['day']: Series = dataset.date.dt.day
    dataset = dataset.loc[dataset.quarter == quarter]

    dataset['month']: Series = dataset.date.dt.month
    dataset['month_name']: Series = dataset.date.dt.month_name()

    month_names = dataset.month_name.unique()
    month_sums = dataset.groupby('month').hash.sum()

    report = {}
    for (month_pk, month_sum), month_name in zip(month_sums.items(), month_names):
        day_list = []
        for day, hash in dataset.loc[dataset.month == month_pk][['day', 'hash']].values:
            day_list.append({int(day): {'total': hash, 'date': f'{month_name[0:3]}. {int(day)}, {year}'}})

        report.update({int(month_pk): day_list, 'date': month_name, 'total': month_sum})

    return {'report': report, 'total': dataset.hash.sum()}
