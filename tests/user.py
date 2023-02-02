import os

from fastapi.testclient import TestClient
import pytest

import setupdb_tests
from app.main import app

client = TestClient(app)


@pytest.fixture()
def root_access_token():
    response = client.post('/users/login', json={'username': 'root_test', 'password': 'qwerty'})
    return response.json()['access_token']


@pytest.fixture()
def admin_access_token():
    response = client.post('/users/login', json={'username': 'admin_test', 'password': 'qwerty'})
    return response.json()['access_token']


@pytest.fixture()
def manager_access_token():
    response = client.post('/users/login', json={'username': 'manager_test', 'password': 'qwerty'})
    return response.json()['access_token']


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


def test_set_inactive_user_good(root_access_token):
    response = client.delete('/users/4', headers={'Authorization': f'Bearer {root_access_token}'})
    assert response.status_code == 202


@pytest.mark.parametrize('access', [admin_access_token, manager_access_token])
def test_set_inactive_user_bad(access):
    response = client.delete('/users/4', headers={'Authorization': f'Bearer {access}'})
    assert response.status_code == 202


@pytest.mark.parametrize('username, password, detail', [['test2', 'qwer', 'Username or password incorrect'],
                                                        ['test', 'qwerty', 'Username or password incorrect'],
                                                        ['test1', 'qwerty', 'Inactive account!']])
def test_login_bad(username, password, detail):
    response = client.post('/users/login', json={'username': username, 'password': password})
    assert response.status_code == 401
    assert response.json()['detail'] == detail


def test_get_user(root_access_token):
    response = client.get('/users', headers={'Authorization': f'Bearer {root_access_token}'})
    assert response.status_code == 200
    assert len(response.json()) == 4

