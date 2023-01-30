import json

import requests


def test(username, password, email):
    data = {
          "username": username,
          "password": password,
          "email": email
            }
    return requests.post('http://localhost:8000/users/', data=json.dumps(data)).text


requests.get('https://google.com')

answer = test('test', 'test', 'test@mail.ru')
print(answer)
answer = test('test2', 'test', 'test@mail.ru')
print(answer)
answer = test('test', 'test', 'test2@mail.ru')
print(answer)
