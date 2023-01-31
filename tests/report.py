import json

import requests


def test(username, password, year, month):
    data = {
        'username': username,
        'password': password
    }

    data2 = {
        'year': year,
        'quarter': month,
        'month': month,
        'output_type': 'pdf'
    }

    response = requests.post('http://localhost:8000/users/login', data=json.dumps(data)).json()
    headers = {'Authorization': f"Bearer {response['access_token']}"}
    # answer = requests.get('http://localhost:8000/reports/dates', data=json.dumps(data2), headers=headers).text
    # print('dates =', answer)

    # answer = requests.post('http://localhost:8000/reports/month_day', data=json.dumps(data2), headers=headers).text
    # print('month_day =', answer)

    answer = requests.post('http://localhost:8000/reports/year_quarter_month', data=json.dumps(data2), headers=headers).text
    print('year_quarter_month =', answer)

    # answer = requests.post('http://localhost:8000/reports/year_quarter', data=json.dumps(data2),
    #                        headers=headers).text
    # print('year_quarter =', answer)

    # answer = requests.post('http://localhost:8000/reports/year_quarter_month_day', data=json.dumps(data2),
    #                        headers=headers).text
    # print('year_quarter_month_day =', answer)

    # answer = requests.post('http://localhost:8000/reports/quarter_month', data=json.dumps(data2),
    #                        headers=headers).text
    # print('quarter_month =', answer)

    # answer = requests.post('http://localhost:8000/reports/quarter_month_day', data=json.dumps(data2),
    #                        headers=headers).text
    # print('quarter_month_day =', answer)


test('eugene', 'qwerty', 2022, 1)

