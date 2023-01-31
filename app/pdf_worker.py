from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from roman import toRoman


def initialize_document(title, data, header_rows=[]):
    doc = SimpleDocTemplate(
        'mypdf.pdf',
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
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
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

    for day, hash, average in dataset[['day', 'hash', 'average']].values:
        table_data.append([f'{month_name[0:3]}. {day}, {year}', year, hash])

    table_data.append(['Totals', year, dataset.hash.sum()])

    title = f'Month by Day Report - {month_name} {year}'

    initialize_document(title, table_data)

    return {'total': float(dataset.hash.sum())}


def year_quarter_month_report(dataset, quarter_groups, months_sum, quarter_sum, year):
    table_data = [['Month', 'Year', 'Month hashrate (EH)']]

    header_rows = []
    row_counter = 1

    for quarter in quarter_groups:
        for month_name in dataset.loc[dataset.quarter == quarter[0]].month_name.unique():
            table_data.append([month_name, year, months_sum.get(month_name)])
            row_counter += 1

        table_data.append([f'{toRoman(quarter[0])} Quarter', year, quarter_sum.get(quarter[0])])
        header_rows.append(row_counter)
        row_counter += 1

    table_data.append(['Totals:', year, dataset.hash.sum()])

    title = f'Year by months/quarters - {year}'

    initialize_document(title, table_data, header_rows)

    return {'total': float(dataset.hash.sum())}


def year_quarter_report(dataset, quarters_sum, year):
    table_data = [['Quarter', 'Year', 'Quarter hashrate (EH)']]

    for quarter_pk, quarter_sum in quarters_sum.items():
        table_data.append([f'{toRoman(quarter_pk)} Quarter', year, quarter_sum])

    table_data.append(['Totals:', year, dataset.hash.sum()])

    title = f'Year by Quarter Report - {year}'

    initialize_document(title, table_data)

    return {'total': float(dataset.hash.sum())}


def year_quarter_month_day_report(dataset, quarter_groups, year, months_sum, quarter_sum, months_sum_average, quarter_sum_average):
    table_data = [['Day/Months/Quarters', 'Average Hashrate (PH/s)', 'Day/Months/Quarters Hashrate (EH)']]

    header_rows = []
    row_counter = 1

    for quarter in quarter_groups:
        for month_name in dataset.loc[dataset.quarter == quarter[0]].month_name.unique():
            for day_ds in dataset.loc[dataset.month_name == month_name][['day', 'hash', 'month_name', 'average']].values:
                table_data.append([f'{month_name} {day_ds[0]}, {year}', day_ds[3], day_ds[1]])
                row_counter += 1

            table_data.append([f'{month_name} Total', months_sum_average.get(month_name), months_sum.get(month_name)])
            header_rows.append(row_counter)
            row_counter += 1

        table_data.append([f'{toRoman(quarter[0])} Quarter', quarter_sum_average.get(quarter[0]),quarter_sum.get(quarter[0])])
        header_rows.append(row_counter)
        row_counter += 1

    table_data.append(['Totals:', dataset.average.sum(), dataset.hash.sum()])

    title = f'Year by day/months/quarters - {year}'

    initialize_document(title, table_data, header_rows)

    return {'total': float(dataset.hash.sum())}


def quarter_month_report(dataset, month_sums, month_names, year, quarter):
    table_data = [['Month', 'Year', 'Months/Quarterly Hashrate (EH)']]

    for (month_pk, month_sum), month_name in zip(month_sums.items(), month_names):
        table_data.append([month_name, year, month_sum])

    table_data.append([f'Totals {toRoman(quarter)} Quarter:', year, dataset.hash.sum()])

    title = f'Quarterly by months/quarters - {toRoman(quarter)} Quarter {year}'

    initialize_document(title, table_data)

    return {'total': float(dataset.hash.sum())}


def quarter_month_day_report(dataset, months_sum, year, quarter):
    table_data = [['Date', 'Year', 'Days/Months Hashrate (EH)']]

    header_rows = []
    row_counter = 1

    for month_name in dataset.month_name.unique():
        for day_ds in dataset.loc[dataset.month_name == month_name][['day', 'hash', 'month_name']].values:
            table_data.append([f'{month_name} {day_ds[0]}, {year}', year, day_ds[1]])
            header_rows.append(row_counter)
            row_counter += 1

        table_data.append([f'{month_name} Total', year, months_sum.get(month_name)])
        header_rows.append(row_counter)
        row_counter += 1

    table_data.append([f'Totals {toRoman(quarter)} Quarter:', year, dataset.hash.sum()])

    title = f'Quarterly by days/months - {toRoman(quarter)} Quarter {year}'

    initialize_document(title, table_data, header_rows)

    return {'total': float(dataset.hash.sum())}

