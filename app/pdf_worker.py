from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle


def month_day_report(dataset, year):
    data = []
    title = 'month_day'
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

    t = Table(
        data,
        colWidths=(width - 70) / 3
    )

    t.setStyle(TableStyle(
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

    t.setStyle(TableStyle(
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
        t.setStyle(TableStyle(
            [
                ('BACKGROUND', (0, i), (-1, i), light_lines if i % 2 != 0 else dark_lines),
            ]
        ))
    t.setStyle(TableStyle(
        [
            ('BACKGROUND', (0, 0), (-1, 0), blueish_gray),
            ('BACKGROUND', (0, -1), (-1, -1), blueish_gray),
        ]
    ))

    elements.append(t)

    doc.build(elements)

    # for day, hash, average, month_name in dataset[['day', 'hash', 'average', 'month_name']].values:
    #     # report.append({'total': hash, 'average': average, 'date': f'{month_name[0:3]}. {day}, {year}'})
    #     pass

    return {'total': float(dataset.hash.sum())}


def year_quarter_month_report(dataset, quarter_groups, months_sum, quarter_sum, year):
    pass


def year_quarter_report(dataset, quarters_sum, year):
    pass


def year_quarter_month_day_report(dataset, quarter_groups, year, months_sum, quarter_sum, months_sum_average, quarter_sum_average):
    pass


def quarter_month_report(dataset, month_sums, month_names, year, quarter):
    pass


def quarter_month_day_report(dataset, months_sum, year, quarter):
    pass

