import json

from fastapi.testclient import TestClient
import requests

from app.main import app

client = TestClient(app)


def test_login():
    response = client.post('/users/login', json={'username': 'test', 'password': 'test'})
    print(response)


# def test(username, password):
#     data = {
#           "username": username,
#           "password": password,
#             }
#     return requests.post('http://localhost:8008/users/login', data=json.dumps(data)).text


test_login()
# answer = test('test', 'test')
# print(answer)
# answer = test('test1', 'test')
# print(answer)
# answer = test('test', 'test2')
# print(answer)
