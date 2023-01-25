import json
from time import sleep

import requests


s = requests.Session()
data = {'username': 'Eugene', 'password': 'qwerty'}
response = requests.post('http://localhost:8000/users/login', data=json.dumps(data)).json()
print(response)
headers = {'Authorization': f"Bearer {response['access_token']}"}

headers_refresh = {'Authorization': f"Bearer {response['refresh_token']}"}

# response = requests.post('http://localhost:8001/company/get', headers=headers).json()
# print(response)
data = {
  "title": "TestCompany",
  "contact_fio": "TestFIO",
  "contact_email": "testmail",
  "contact_phone": "test_phone",
  "img_logo": "test_logo",
  "description": "test description"
}

data2 = {
  "company_id": 1,
  "user_id": 1
}

data3 = {
  "date": "2023-01-23",
  "average": 10,
  "hash": 35,
  "company_id": 1
}

# response = requests.post('http://localhost:8000/companies/create', data=json.dumps(data), headers=headers).json()
# print(response)
# response = requests.post('http://localhost:8000/users/add_company', data=json.dumps(data2), headers=headers).json()
# print(response)
# response = requests.post('http://localhost:8000/hashrates/me', data=json.dumps(data3), headers=headers).json()
# response = requests.get('http://localhost:8000/hashrates/company/1', headers=headers).json()
# print(response)

# file = {'file':  open('test_hr.xls', 'rb'), "company_id": 1}
# data4 = {'file_format': 'json', 'year': 2022}
# response = requests.post('http://localhost:8000/hashrates/get_report', data=json.dumps(data4), headers=headers).text
#

sleep(1)

response = requests.get('http://localhost:8000/token/', headers=headers).text

print(response)

# response = requests.post('http://localhost:8000/token/refresh', headers=headers_refresh)


# print(response)
