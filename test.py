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
  "email": "Test@gmail.com",
  "password": "qwerty",
  "role": "manager",
  "company_id": 0
}
# response = requests.post('http://localhost:8001/company/create', data=json.dumps(data), headers=headers).json()
# print(response)
# response = requests.post('http://localhost:8000/user/create', data=json.dumps(data), headers=headers).json()
# print(response)
response = requests.delete('http://localhost:8000/user/ban?user_id=2', headers=headers).json()
print(response)


