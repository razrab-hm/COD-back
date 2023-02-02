from fastapi.testclient import TestClient
import pytest

from app.main import app


client = TestClient(app)


def test_good_register():
    data = {
        'username': 'test',
        'email': 'email@mail.ru',
        'password': 'qwerty'
    }
    response = client.post('/users', json=data)
    print(response)
    assert response.status_code == 201


def test_bad_register():
    data = {
        'username': 'test',
        'email': 'email@mail.ru',
        'password': 'qwerty'
    }

    response = client.post('/users', json=data)
    print(response)
    assert response.status_code == 407

    data = {
        'username': 'test',
        'email': 'lol',
        'password': 'qwerty'
    }

    response = client.post('/users', json=data)
    print(response)
    assert response.status_code == 406


def test_login():
    response = client.post('/users/login', json={'username': 'test', 'password': 'qwerty'})
    print(response)
    assert response.status_code == 202


