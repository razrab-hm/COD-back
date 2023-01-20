import json

import requests


s = requests.Session()
data = {'email': 'Eugene', 'password': 'qwerty'}
response = requests.post('http://localhost:8000/user/login', data=json.dumps(data)).json()
print(response)
headers = {'Authorization': f"Bearer {response['access_token']}"}

# response = requests.post('http://localhost:8001/company/get', headers=headers).json()
# print(response)
data = {
  "id": 6,
  "email": "test2",
  "password": "123456",
  "role": "admin",
}
# response = requests.post('http://localhost:8001/company/create', data=json.dumps(data), headers=headers).json()
# print(response)
response = requests.put('http://localhost:8000/user/update', data=json.dumps(data), headers=headers).json()
print(response)
