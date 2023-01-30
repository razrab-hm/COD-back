def month_day_report(dataset, year):
    report = []

    for day, hash, average, month_name in dataset[['day', 'hash', 'average', 'month_name']].values:
        report.append({'total': hash, 'average': average, 'date': f'{month_name[0:3]}. {day}, {year}'})

    return {'report': report, 'total': dataset.hash.sum()}


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

