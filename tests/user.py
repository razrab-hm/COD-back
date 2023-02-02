import os

from fastapi.testclient import TestClient
import pytest

import superuser
from app.main import app

client = TestClient(app)
superuser.create_to_test()


@pytest.mark.parametrize('username, email, password', [('test1', 'test1@mail.ru', 'qwerty'),
                                                       ('test2', 'test2@gmail.com', 'qwerty'),
                                                       ('test3', 'test3@gmail.com', 'qwerty')])
def test_register_good(username, email, password):
    data = {
        'username': username,
        'email': email,
        'password': password
    }
    response = client.post('/users', json=data)
    assert response.status_code == 201


@pytest.mark.parametrize('username, email, password, detail', [['test1', 'abc@mail.ru', 'qwerty', 'Username already registered'],
                                                               ['test4', 'test1@mail.ru', 'qwerty', 'Email already registered'],
                                                               ['test5', 'unvalidmail1', 'qwerty', 'Email is not valid'],
                                                               ['test6', 'unvalidmail2@mail', 'qwerty', 'Email is not valid']])
def test_register_bad(username, email, password, detail):
    data = {
        'username': username,
        'email': email,
        'password': password
    }

    response = client.post('/users', json=data)
    assert response.status_code == 406
    assert response.json()['detail'] == detail


def test_login_good():
    response = client.post('/users/login', json={'username': 'test1', 'password': 'qwerty'})
    print(response)
    assert response.status_code == 202


def test_set_inactive_user(admin_access_token):
    response = client.delete('/users/2', headers={'Authorization': f'Bearer {admin_access_token}'})
    assert response.status_code == 202


@pytest.mark.parametrize('username, password, detail', [['test2', 'qwer', 'Username or password incorrect'],
                                                        ['test', 'qwerty', 'Username or password incorrect'],
                                                        ['test1', 'qwerty', 'Inactive account!']])
def test_login_bad(username, password, detail):
    response = client.post('/users/login', json={'username': username, 'password': password})
    assert response.status_code == 401
    assert response.json()['detail'] == detail


def test_get_user(admin_access_token):
    response = client.get('/users', headers={'Authorization': f'Bearer {admin_access_token}'})
    assert response.status_code == 200
    assert len(response.json()) == 4


@pytest.fixture()
def admin_access_token():
    response = client.post('/users/login', json={'username': 'root_test', 'password': 'qwerty'})
    return response.json()['access_token']


