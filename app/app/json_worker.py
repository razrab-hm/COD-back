from roman import toRoman


def month_day_report(dataset, year):
    report = []

    date_hash_sum = dataset.groupby('date').hash.sum()
    date_average_sum = dataset.groupby('date').average.sum()

    dates = []

    for day, hash, average, month_name, date in dataset[['day', 'hash', 'average', 'month_name', 'date']].values:
        if date not in dates:
            report.append({'total': f"{round(date_hash_sum.get(date), 2):_.2f}".replace("_", " "), 'average': f"{round(date_average_sum.get(date), 3):_.3f}".replace("_", ""), 'date': f'{month_name[0:3]}. {day}, {year}'})
            dates.append(date)

    return {'report': report, 'total': f"{round(float(dataset.hash.sum()), 2):_.2f}".replace("_", ""), 'year': year}


def year_quarter_month_report(dataset, quarter_groups, months_sum, quarter_sum, year):
    report = []

    for quarter in quarter_groups:
        for month_name in dataset.loc[dataset.quarter == quarter[0]].month_name.unique():
            report.append({'type': 'month', 'date': f'{month_name}', 'total': f"{round(months_sum.get(month_name), 2):_.2f}".replace("_", "")})

        report.append({'type': 'quarter', 'date': f'{toRoman(quarter[0])} Quarter', 'total': f"{round(quarter_sum.get(quarter[0]), 2):_.2f}".replace("_", "")})

    return {'report': report, 'total': f"{round(float(dataset.hash.sum()), 2):_.2f}".replace("_", ""), 'year': year}


def year_quarter_report(dataset, quarters_sum, year):
    report = []

    for quarter_pk, quarter_sum in quarters_sum.items():
        report.append({'total': f"{round(quarter_sum, 2):_.2f}".replace("_", " "), 'Quarter': quarter_pk})

    return {'report': report, 'total': f"{round(float(dataset.hash.sum()), 2):_.2f}".replace("_", " "), 'year': year}


def year_quarter_month_day_report(dataset, quarter_groups, year, months_sum, quarter_sum, months_sum_average, quarter_sum_average):
    report = []

    date_hash_sum = dataset.groupby('date').hash.sum()
    date_average_sum = dataset.groupby('date').average.sum()

    dates = []

    for quarter in quarter_groups:
        for month_name in dataset.loc[dataset.quarter == quarter[0]].month_name.unique():
            for day_ds in dataset.loc[dataset.month_name == month_name][['day', 'hash', 'month_name', 'average', 'date']].values:
                if day_ds[4] not in dates:
                    report.append({'type': 'day', 'date': f'{day_ds[2][0:3]}. {day_ds[0]}, {year}', 'average': f"{round(date_average_sum.get(day_ds[4]), 3):_.3f}".replace("_", ""),
                                   'hash': f"{round(date_hash_sum.get(day_ds[4]), 2):_.2f}".replace("_", "")})
                    dates.append(day_ds[4])

            report.append({'type': 'month', 'date': f'{month_name}', 'total': f"{round(months_sum.get(month_name), 2):_.2f}".replace("_", ""),
                           'average': f"{round(months_sum_average.get(month_name), 3):_.3f}".replace("_", "")})

        report.append({'type': 'quarter', 'date': f'{toRoman(quarter[0])} quarter', 'total': f"{round(quarter_sum.get(quarter[0]), 2):_.2f}".replace("_", ""), 'average': f"{round(quarter_sum_average.get(quarter[0]), 3):_.3f}".replace("_", "")})

    return {'report': report, 'total': f"{round(float(dataset.hash.sum()), 2):_.2f}".replace("_", ""), 'year': year}


def quarter_month_report(dataset, month_sums, month_names, year, quarter):
    report = []
    for (month_pk, month_sum), month_name in zip(month_sums.items(), month_names):
        report.append({'date': month_name, 'total': f"{round(month_sum, 2):_.2f}".replace("_", "")})

    return {'report': report, 'total': f"{round(float(dataset.hash.sum()), 2):_.2f}".replace("_", ""), 'year': year, 'quarter': quarter}


def quarter_month_day_report(dataset, months_sum, year, quarter):
    report = []

    date_hash_sum = dataset.groupby('date').hash.sum()

    dates = []

    for month_name in dataset.month_name.unique():
        for day_ds in dataset.loc[dataset.month_name == month_name][['day', 'hash', 'month_name', 'date']].values:
            if day_ds[3] not in dates:
                report.append({'type': 'day', 'date': f'{day_ds[2]}, {day_ds[0]}', 'hash': f"{round(date_hash_sum.get(day_ds[3]), 2):_.2f}".replace("_", "")})
                dates.append(day_ds[3])

        report.append({'type': 'month', 'date': f'{month_name}', 'total': f"{round(months_sum.get(month_name), 2):_.2f}".replace("_", "")})

    return {'report': report, 'total': f"{round(float(dataset.hash.sum()), 2):_.2f}".replace("_", ""), 'year': year, 'quarter': quarter}



