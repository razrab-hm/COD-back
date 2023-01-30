import pandas as pd
from fastapi import UploadFile
from pandas import DataFrame


def get_xls_data(file: UploadFile):
    xls = pd.ExcelFile(file.file)
    sheet: DataFrame = xls.parse(0)
    print(zip(sheet[0], sheet[1]))
    return zip(sheet['Date'], sheet['Hashrate'])

