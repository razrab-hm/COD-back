import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.tests import conftest

client = TestClient(app)


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
    print(response)
    assert response.status_code == 201


@pytest.mark.parametrize('username, email, password, detail', [['user', 'abc@mail.ru', 'qwerty', 'Username already registered'],
                                                               ['user2', 'user@mail.ru', 'qwerty', 'Email already registered'],
                                                               ['user2', 'unvalidmail1', 'qwerty', 'Email is not valid'],
                                                               ['user2', 'unvalidmail2@mail', 'qwerty', 'Email is not valid']])
def test_register_bad(username, email, password, detail):
    conftest.user()
    data = {
        'username': username,
        'email': email,
        'password': password
    }

    response = client.post('/users', json=data)
    assert response.status_code == 406
    assert response.json()['detail'] == detail


def test_login_good():
    user = conftest.user()
    response = client.post('/users/login', json={'username': user.username, 'password': 'qwerty'})
    print(response)
    assert response.status_code == 202


@pytest.mark.parametrize('username, password, detail', [['test2', 'qwer', 'Username or password incorrect'],
                                                        ['test', 'qwerty', 'Username or password incorrect']])
def test_login_bad(username, password, detail):
    response = client.post('/users/login', json={'username': username, 'password': password})
    assert response.status_code == 401
    assert response.json()['detail'] == detail


def test_login_inactive_bad():
    user = conftest.inactive_user()
    response = client.post('/users/login', json={'username': user.username, 'password': 'qwerty'})
    assert response.status_code == 401
    assert response.json()['detail'] == 'Inactive account!'


def test_update_user_good():
    admin = conftest.admin_user()
    user = conftest.user()
    headers = conftest.auth_user(admin)
    update_data = {
          "username": "123",
          "password": "123",
          "id": user.id,
          "email": "123",
          "role": "root"}

    response = client.put('/users', headers=headers, json=update_data)

    assert response.json() == 1


