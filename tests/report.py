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
        'output_type': 'json'
    }

    response = requests.post('http://localhost:8000/users/login', data=json.dumps(data)).json()
    print(response)
    headers = {'Authorization': f"Bearer {response['access_token']}"}
    return requests.post('http://localhost:8000/hashrates/quarter_month_day', data=json.dumps(data2), headers=headers).text


answer = test('Eugene', 'qwerty', 2022, 1)
print(answer)
