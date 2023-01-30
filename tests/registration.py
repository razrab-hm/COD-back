import json

import requests


def test(username, password, email):
    data = {
          "username": username,
          "password": password,
          "email": email
            }
    return requests.post('http://127.0.0.1:8000/users/', data=json.dumps(data)).text


print(requests.get('https://google.com').text)
print(requests.post('https://google.com').text)

answer = test('test', 'test', 'test@mail.ru')
print(answer)
answer = test('test2', 'test', 'test@mail.ru')
print(answer)
answer = test('test', 'test', 'test2@mail.ru')
print(answer)
