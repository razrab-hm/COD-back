import json

import requests


def test(username, password):
    data = {
          "username": username,
          "password": password,
            }
    return requests.post('http://localhost:8000/users/login', data=json.dumps(data)).text


answer = test('test', 'test')
print(answer)
answer = test('test1', 'test')
print(answer)
answer = test('test', 'test2')
print(answer)
