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
        'output_type': 'json'
    }

    response = requests.post('http://localhost:8000/users/login', data=json.dumps(data)).json()
    print(response)
    headers = {'Authorization': f"Bearer {response['access_token']}"}
    # answer = requests.post('http://localhost:8000/hashrates/month_day', data=json.dumps(data2), headers=headers).text
    # print('month_day = ', answer)
    answer = requests.post('http://localhost:8000/hashrates/year_quarter_month', data=json.dumps(data2), headers=headers).text
    print('year_quarter_month', answer)
    # answer = requests.post('http://localhost:8000/hashrates/year_quarter', data=json.dumps(data2),
    #                        headers=headers).text
    # print('year_quarter = ', answer)
    # answer = requests.post('http://localhost:8000/hashrates/year_quarter_month_day', data=json.dumps(data2),
    #                        headers=headers).text
    # print('year_quarter_month_day = ', answer)
    # answer = requests.post('http://localhost:8000/hashrates/quarter_month', data=json.dumps(data2),
    #                        headers=headers).text
    # print('quarter_month = ', answer)
    # answer = requests.post('http://localhost:8000/hashrates/quarter_month_day', data=json.dumps(data2),
    #                        headers=headers).text
    # print('quarter_month_day = ', answer)


test('Eugene', 'qwerty', 2022, 1)

