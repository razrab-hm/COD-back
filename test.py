import json

import requests


s = requests.Session()
data = {'email': 'Eugene', 'password': 'qwerty'}
response = requests.post('http://localhost:8001/user/login', data=json.dumps(data)).json()
print(response)
headers = {'Authorization': f"Bearer {response['access_token']}"}

# response = requests.post('http://localhost:8001/company/get', headers=headers).json()
# print(response)
# data = {
#   "name": "Test2",
#   "contact_name": "Test",
#   "contact_email": "Test"
# }
# response = requests.post('http://localhost:8001/company/create', data=json.dumps(data), headers=headers).json()
# print(response)
response = requests.post('http://localhost:8001/user/set_company?email=Eugene&company_id=2', headers=headers).json()
print(response)
