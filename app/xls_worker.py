import openpyxl
import pandas as pd
from fastapi import UploadFile
from openpyxl.worksheet.worksheet import Worksheet
from pandas import DataFrame


def get_xls_data(file: UploadFile):
    xls = pd.ExcelFile(file.file)
    sheet: DataFrame = xls.parse(0)
    if type(sheet.values[0][0]) == str:
        return zip(sheet[sheet.keys()[0]], sheet[sheet.keys()[1]])
    else:
        return zip(sheet[sheet.keys()[1]], sheet[sheet.keys()[0]])


def month_day_report(dataset, year):
    report = []

    wb = openpyxl.Workbook()
    ws: Worksheet = wb.active
    row_counter = 1

    ws.column_dimensions['A'].width = 30
    ws.column_dimensions['B'].width = 15
    ws.column_dimensions['C'].width = 40

    ws.cell(row=row_counter, column=1, value='Date')
    ws.cell(row=row_counter, column=2, value='Year')
    ws.cell(row=row_counter, column=3, value='Days Hashrate (EH)')
    row_counter += 1

    for day, hash, average, month_name in dataset[['day', 'hash', 'average', 'month_name']].values:
        ws.cell(row=row_counter, column=1, value=f'{month_name} {day}, {year}')
        ws.cell(row=row_counter, column=2, value=year)
        ws.cell(row=row_counter, column=3, value=hash)
        row_counter += 1

    ws.cell(row=row_counter, column=1, value=f'Totals:')
    ws.cell(row=row_counter, column=2, value=year)
    ws.cell(row=row_counter, column=3, value=dataset.hash.sum())

    wb.save("sample.xlsx")

    return {'report': report, 'total': dataset.hash.sum()}


def year_quarter_month_report():
    pass


def year_quarter_report():
    pass


def year_quarter_month_day_report():
    pass


def quarter_month_report():
    pass


def quarter_month_day_report():
    pass
