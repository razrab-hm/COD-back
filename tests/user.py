from fastapi.testclient import TestClient
import pytest

import superuser
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
    assert response.status_code == 406

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


def test_bad_login():
    response = client.post('/users/login', json={'username': 'eugene', 'password': 'qwerty'})
    print(response)
    assert response.status_code == 202


@pytest.fixture()
def create_admin():
    user = superuser.create_to_test()
    print(user)
    return user


@pytest.fixture()
def access_token():
    response = client.post('/users/login', json={'username': 'root_test', 'password': 'qwerty'})
    return response.json()['access_token']


@pytest.fixture()
def admin(create_admin):
    return create_admin


def test_get_user(admin, access_token):
    response = client.get('/users', headers={'Authorization': f'Bearer {access_token}'})
    assert response.json() == 1


