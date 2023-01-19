import json

import requests


s = requests.Session()
data = {'email': 'test10', 'password': 'test'}
response = requests.post('http://localhost:8000/user/login', data=json.dumps(data)).json()
print(response)
headers = {'Authorization': f"Bearer {response['access_token']}"}

response = requests.get('http://localhost:8000/user/user', headers=headers).json()
print(response)
