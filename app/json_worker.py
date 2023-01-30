from roman import toRoman


def month_day_report(dataset, year):
    report = []

    for day, hash, average, month_name in dataset[['day', 'hash', 'average', 'month_name']].values:
        report.append({'total': hash, 'average': average, 'date': f'{month_name[0:3]}. {day}, {year}', 'year': year})

    return {'report': report, 'total': dataset.hash.sum()}


def year_quarter_month_report(dataset, quarter_groups, months_sum, quarter_sum):
    report = []

    for quarter in quarter_groups:
        for month_name in dataset.loc[dataset.quarter == quarter[0]].month_name.unique():
            report.append({'type': 'month', 'date': f'{month_name}', 'total': months_sum.get(month_name)})

        report.append(
            {'type': 'quarter', 'date': f'{toRoman(quarter[0])} quarter', 'total': quarter_sum.get(quarter[0])})

    return {'report': report, 'total': dataset.hash.sum()}


def year_quarter_report():
    report = []

    for quarter_pk, quarter_sum in quarters_sum.items():
        print(quarter_pk, quarter_sum)
        report.append({'total': quarter_sum, 'quarter': quarter_pk})

    return {'report': report, 'total': dataset.hash.sum()}


def year_quarter_month_day_report():
    report = []

    for quarter in quarter_groups:
        for month_name in dataset.loc[dataset.quarter == quarter[0]].month_name.unique():
            for day_ds in dataset.loc[dataset.month_name == month_name][
                ['day', 'hash', 'month_name', 'average']].values:
                report.append({'type': 'day', 'date': f'{day_ds[2][0:3]}. {day_ds[0]}, {year}', 'average': day_ds[3],
                               'hash': day_ds[1]})

            report.append({'type': 'month', 'date': f'{month_name}', 'total': months_sum.get(month_name)})

        report.append(
            {'type': 'quarter', 'date': f'{toRoman(quarter[0])} quarter', 'total': quarter_sum.get(quarter[0])})

    return {'report': report, 'total': dataset.hash.sum()}


def quarter_month_report():
    report = []
    for (month_pk, month_sum), month_name in zip(month_sums.items(), month_names):
        report.append({int(month_pk): {'date': month_name, 'total': month_sum}})

    return {'report': report, 'total': dataset.hash.sum()}


def quarter_month_day_report():
    report = []

    for month_name in dataset.month_name.unique():
        for day_ds in dataset.loc[dataset.month_name == month_name][['day', 'hash', 'month_name']].values:
            report.append({'type': 'day', 'date': f'{day_ds[2]}, {day_ds[0]}', 'hash': day_ds[1]})

        report.append({'type': 'month', 'date': f'{month_name}', 'total': months_sum.get(month_name)})

    return {'report': report, 'total': dataset.hash.sum()}



