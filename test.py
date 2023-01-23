import json

import requests


s = requests.Session()
data = {'email': 'Eugene', 'password': 'qwerty'}
response = requests.post('http://localhost:8000/users/login', data=json.dumps(data)).json()
print(response)
headers = {'Authorization': f"Bearer {response['access_token']}"}

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
  "user_id": 4
}
# response = requests.post('http://localhost:8000/companies/create', data=json.dumps(data), headers=headers).json()
# print(response)
# response = requests.post('http://localhost:8000/users/add_company', data=json.dumps(data2), headers=headers).json()
# print(response)
response = requests.get('http://localhost:8000/users/companies/1', headers=headers).json()
print(response)


