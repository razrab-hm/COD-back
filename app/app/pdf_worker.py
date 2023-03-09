import random
import threading

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from roman import toRoman
from fastapi.responses import FileResponse


def initialize_document(title, data, savefile, header_rows=[]):
    doc = SimpleDocTemplate(
        savefile,
        pagesize=A4,
        topMargin=9
    )

    width, height = A4
    elements = []

    style = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'title_style',
        fontName="Helvetica-Bold",
        fontSize=13,
        parent=style['Heading2'],
        alignment=1,
        spaceAfter=8)

    title = Paragraph(title, title_style)
    elements.append(title)

    table = Table(
        data,
        colWidths=(width - 70) / 3
    )

    table.setStyle(TableStyle(
        [
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('ALIGN', (-1, 0), (-1, -1), 'RIGHT'),
        ]
    ))

    border = colors.Color(0.819, 0.827, 0.839, alpha=1)
    border_thickness = 1.5
    light_lines = colors.Color(1, 1, 1, alpha=1)
    dark_lines = colors.Color(0.878, 0.878, 0.878, alpha=1)
    blueish_gray = colors.Color(0.862, 0.874, 0.89, alpha=1)

    table.setStyle(TableStyle(
        [
            ('LINEABOVE', (0, 0), (-1, 0), border_thickness, border),  # обводка таблицы сверху
            ('LINEBELOW', (0, -1), (-1, -1), border_thickness, border),  # обводка таблицы снизу
            ('LINEBEFORE', (0, 0), (0, -1), border_thickness, border),  # обводка таблицы слева
            ('LINEAFTER', (-1, 0), (-1, -1), border_thickness, border),  # обводка таблицы справа

            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # первая строка жирным
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),  # последняя строка жирным
        ]
    ))

    for i in range(1, len(data)):
        if i not in header_rows:
            table.setStyle(TableStyle(
                [
                    ('BACKGROUND', (0, i), (-1, i), light_lines if i % 2 != 0 else dark_lines),
                ]
            ))
        else:
            table.setStyle(TableStyle(
                [
                    ('BACKGROUND', (0, i), (-1, i), blueish_gray),
                    ('FONTNAME', (0, i), (-1, i), 'Helvetica-Bold'),
                ]
            ))

    table.setStyle(TableStyle(
        [
            ('BACKGROUND', (0, 0), (-1, 0), blueish_gray),
            ('BACKGROUND', (0, -1), (-1, -1), blueish_gray),
        ]
    ))

    elements.append(table)

    doc.build(elements)


def month_day_report(dataset, year):
    month_name = dataset.month_name.unique()[0]

    table_data = [['Date', 'Year', 'Days Hashrate (EH)']]

    date_hash_sum = dataset.groupby('date').hash.sum()

    dates = []

    for day, hash, average, date in dataset[['day', 'hash', 'average', 'date']].values:
        if date not in dates:
            table_data.append([f'{month_name[0:3]}. {day}, {year}', year, f"{round(date_hash_sum.get(date), 2):_.2f}".replace("_", " ")])
            dates.append(date)

    table_data.append(['Totals', year, f"{round(dataset.hash.sum(), 2):_.2f}".replace("_", " ")])

    title = f'Month by Day Report - {month_name} {year}'

    savefile = f'files/pdf{random.randint(0, 100)}.pdf'

    initialize_document(title, table_data, savefile=savefile)
    return FileResponse(savefile)


def year_quarter_month_report(dataset, quarter_groups, months_sum, quarter_sum, year):
    table_data = [['Month', 'Year', 'Month hashrate (EH)']]

    header_rows = []
    row_counter = 1

    for quarter in quarter_groups:
        for month_name in dataset.loc[dataset.quarter == quarter[0]].month_name.unique():
            table_data.append([month_name, year, f"{round(months_sum.get(month_name), 2):_.2f}".replace("_", " ")])
            row_counter += 1

        table_data.append([f'{toRoman(quarter[0])} Quarter', year, f"{round(quarter_sum.get(quarter[0]), 2):_.2f}".replace("_", " ")])
        header_rows.append(row_counter)
        row_counter += 1

    table_data.append(['Totals:', year, f"{round(dataset.hash.sum(), 2):_.2f}".replace("_", " ")])

    title = f'Year by months/quarters - {year}'

    savefile = f'files/pdf{random.randint(0, 100)}.pdf'

    initialize_document(title, table_data, header_rows=header_rows, savefile=savefile)
    return FileResponse(savefile)


def year_quarter_report(dataset, quarters_sum, year):
    table_data = [['Quarter', 'Year', 'Quarter hashrate (EH)']]

    for quarter_pk, quarter_sum in quarters_sum.items():
        table_data.append([f'{toRoman(quarter_pk)} Quarter', year, f"{round(quarter_sum, 2):_.2f}".replace("_", " ")])

    table_data.append(['Totals:', year, f"{round(dataset.hash.sum(), 2):_.2f}".replace("_", " ")])

    title = f'Year by Quarter Report - {year}'

    savefile = f'files/pdf{random.randint(0, 100)}.pdf'

    initialize_document(title, table_data, savefile=savefile)
    return FileResponse(savefile)


def year_quarter_month_day_report(dataset, quarter_groups, year, months_sum, quarter_sum, months_sum_average, quarter_sum_average):
    table_data = [['Day/Months/Quarters', 'Average Hashrate (PH/s)', 'Day/Months/Quarters Hashrate (EH)']]

    header_rows = []
    row_counter = 1

    date_hash_sum = dataset.groupby('date').hash.sum()
    date_average_sum = dataset.groupby('date').average.sum()

    dates = []

    for quarter in quarter_groups:
        for month_name in dataset.loc[dataset.quarter == quarter[0]].month_name.unique():
            for day_ds in dataset.loc[dataset.month_name == month_name][['day', 'hash', 'month_name', 'average', 'date']].values:
                if day_ds[4] not in dates:
                    table_data.append([f'{month_name} {day_ds[0]}, {year}', f"{round(date_average_sum.get(day_ds[4]), 3):_.3f}".replace("_", " "), f"{round(date_hash_sum.get(day_ds[4]), 2):_.2f}".replace("_", " ")])
                    row_counter += 1
                    dates.append(day_ds[4])

            table_data.append([f'{month_name} Total', f"{round(months_sum_average.get(month_name), 3):_.3f}".replace("_", " "), f"{round(months_sum.get(month_name), 2):_.2f}".replace("_", " ")])
            header_rows.append(row_counter)
            row_counter += 1

        table_data.append([f'{toRoman(quarter[0])} Quarter', f"{round(quarter_sum_average.get(quarter[0]), 3):_.3f}".replace("_", " "), f"{round(quarter_sum.get(quarter[0]), 2):_.2f}".replace("_", " ")])
        header_rows.append(row_counter)
        row_counter += 1

    table_data.append(['Totals:', f"{round(dataset.average.sum(), 3):_.3f}".replace("_", " "), f"{round(dataset.hash.sum(), 2):_.2f}".replace("_", " ")])

    title = f'Year by day/months/quarters - {year}'

    savefile = f'files/pdf{random.randint(0, 100)}.pdf'

    initialize_document(title, table_data, header_rows=header_rows, savefile=savefile)
    return FileResponse(savefile)


def quarter_month_report(dataset, month_sums, month_names, year, quarter):
    table_data = [['Month', 'Year', 'Months/Quarterly Hashrate (EH)']]

    for (month_pk, month_sum), month_name in zip(month_sums.items(), month_names):
        table_data.append([month_name, year, f"{round(month_sum, 2):_.2f}".replace("_", " ")])

    table_data.append([f'Totals {toRoman(quarter)} Quarter:', year, f"{round(dataset.hash.sum(), 2):_.2f}".replace("_", " ")])

    title = f'Quarterly by months/quarters - {toRoman(quarter)} Quarter {year}'

    savefile = f'files/pdf{random.randint(0, 100)}.pdf'

    initialize_document(title, table_data, savefile=savefile)
    return FileResponse(savefile)


def quarter_month_day_report(dataset, months_sum, year, quarter):
    table_data = [['Date', 'Year', 'Days/Months Hashrate (EH)']]

    header_rows = []
    row_counter = 1

    date_hash_sum = dataset.groupby('date').hash.sum()

    dates = []

    for month_name in dataset.month_name.unique():
        for day_ds in dataset.loc[dataset.month_name == month_name][['day', 'hash', 'month_name', 'date']].values:
            if day_ds[3] not in dates:
                table_data.append([f'{month_name} {day_ds[0]}, {year}', year, f"{round(date_hash_sum.get(day_ds[3]), 2):_.2f}".replace("_", " ")])
                row_counter += 1
                dates.append(day_ds[3])

        table_data.append([f'{month_name} Total', year, f"{round(months_sum.get(month_name), 2):_.2f}".replace("_", " ")])
        header_rows.append(row_counter)
        row_counter += 1

    table_data.append([f'Totals {toRoman(quarter)} Quarter:', year, f"{round(dataset.hash.sum(), 2):_.2f}".replace("_", " ")])

    title = f'Quarterly by days/months - {toRoman(quarter)} Quarter {year}'

    savefile = f'files/pdf{random.randint(0, 100)}.pdf'

    initialize_document(title, table_data, header_rows=header_rows, savefile=savefile)
    return FileResponse(savefile)
