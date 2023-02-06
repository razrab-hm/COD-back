import json

import requests


s = requests.Session()
data = {'username': 'eugene', 'password': 'qwerty'}
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

# response = requests.post('http://localhost:8000/companies/', data=json.dumps(data), headers=headers).json()
# print(response)

# response = requests.post('http://localhost:8000/users/add_company', data=json.dumps(data2), headers=headers).json()
# print(response)
# response = requests.post('http://localhost:8000/hashrates/me', data=json.dumps(data3), headers=headers).json()
# response = requests.get('http://localhost:8000/hashrates/company/1', headers=headers).json()
# print(response)

file = {'file':  open('test_hr.xls', 'rb')}
# data4 = {'file_format': 'json', 'year': 2022}
response = requests.post('http://localhost:8000/hashrates/import/2', files=file, headers=headers).text

print(response)

# sleep(1)
#
# data5 = {
#   'year': 2022,
#   'month': 1,
#   'output_type': '1'
# }
#
# response = requests.post('http://localhost:8000/hashrates/month_day', data=json.dumps(data5), headers=headers).text
#
# response = requests.get('http://localhost:8000/users/inactive', headers=headers).text
#
# print(response)

# response = requests.post('http://localhost:8000/token/refresh', headers=headers_refresh)


# print(response)
