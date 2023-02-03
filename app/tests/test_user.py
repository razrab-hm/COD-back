import pytest

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
from app.tests import conftest, company_creator
from app.tests import user_creator


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
    user_creator.user()
    data = {
        'username': username,
        'email': email,
        'password': password
    }

    response = client.post('/users', json=data)
    assert response.status_code == 406
    assert response.json()['detail'] == detail


def test_login_good():
    user = user_creator.user()
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
    user = user_creator.inactive_user()
    response = client.post('/users/login', json={'username': user.username, 'password': 'qwerty'})
    assert response.status_code == 401
    assert response.json()['detail'] == 'Inactive account!'


@pytest.mark.parametrize('updater, to_update', [
    [user_creator.root_user, user_creator.user],
    [user_creator.admin_user, user_creator.user],
    [user_creator.root_user, user_creator.admin_user]
])
def test_update_user_good(updater, to_update):
    updater = updater('user1')
    to_update = to_update('user2')
    headers = conftest.auth_user(updater)
    update_data = {
          "username": "123",
          "password": "123",
          "id": to_update.id,
          "email": "123",
          "role": "admin"}

    response = client.put('/users', headers=headers, json=update_data)

    res_data = response.json()
    res_data.pop('hash_password')
    res_data.pop('inactive')
    update_data.pop('password')

    assert response.status_code == 200
    assert res_data == update_data


@pytest.mark.parametrize('updater, to_update', [
    [user_creator.admin_user, user_creator.admin_user],
    [user_creator.user, user_creator.user],
    [user_creator.user, user_creator.admin_user],
    [user_creator.admin_user, user_creator.user]
])
def test_update_user_bad(updater, to_update):
    updater = updater('user1')
    to_update = to_update('user2')
    headers = conftest.auth_user(updater)
    update_data = {
        "username": "123",
        "password": "123",
        "id": to_update.id,
        "email": "123",
        "role": "root"}

    response = client.put('/users', headers=headers, json=update_data)

    assert response.json()['detail'] == "You don't have permissions"
    assert response.status_code == 406


def test_update_user_username_bad():
    updater = user_creator.root_user()
    to_update = user_creator.user()
    user = user_creator.user('user2')

    headers = conftest.auth_user(updater)
    update_data = {
        "username": "user2",
        "id": to_update.id}

    response = client.put('/users', headers=headers, json=update_data)

    assert response.json()['detail'] == "User already exists"
    assert response.status_code == 409


def test_change_user_password_good():
    user = user_creator.user()
    headers = conftest.auth_user(user)
    update_data = {
        "id": user.id,
        "password": 'qwer'
    }
    response = client.put('/users', headers=headers, json=update_data)
    res_data = response.json()
    res_data.pop('hash_password')
    res_data.pop('inactive')
    update_data.pop('password')

    assert res_data['id'] == update_data['id']
    assert response.status_code == 200


def test_change_user_password_bad():
    user = user_creator.user()
    user2 = user_creator.user('user2')
    headers = conftest.auth_user(user)
    update_data = {
        "id": user2.id,
        "password": 'qwer'
    }
    response = client.put('/users', headers=headers, json=update_data)
    res_data = response.json()

    assert res_data['detail'] == "You don't have permissions"
    assert response.status_code == 406


@pytest.mark.parametrize('checker, user', [[user_creator.root_user, user_creator.user],
                                           [user_creator.admin_user, user_creator.user]])
def test_get_users_good(checker, user):
    company_creator.company()

    checker = checker(company=1)
    user = user(company=1)

    headers = conftest.auth_user(checker)

    response = client.get('/users', headers=headers)

    assert len(response.json()) == 2
    assert response.status_code == 200


def test_get_users_bad():
    company_creator.company()
    user = user_creator.user(company=1)

    headers = conftest.auth_user(user)

    response = client.get('/users', headers=headers)

    assert response.json() == []
    assert response.status_code == 200


@pytest.mark.parametrize('checker, user', [[user_creator.root_user, user_creator.user],
                                           [user_creator.admin_user, user_creator.user]])
def test_get_user_by_id_good(checker, user):
    company_creator.company()

    checker = checker(company=1)
    user = user(company=1)

    headers = conftest.auth_user(checker)

    response = client.get(f'/users/{user.id}', headers=headers)

    assert response.json()['id'] == user.id
    assert response.status_code == 200


def test_get_user_by_id_bad():
    company_creator.company()

    checker = user_creator.user(company=1)
    user = user_creator.user(company=1, username='user2')

    headers = conftest.auth_user(checker)

    response = client.get(f'/users/{user.id}', headers=headers)

    assert response.json() == None
    assert response.status_code == 200


@pytest.mark.parametrize('root, user', [
    [user_creator.root_user, user_creator.user],
    [user_creator.root_user, user_creator.admin_user],
    [user_creator.admin_user, user_creator.user]
])
def test_set_inactive_user_good(root, user):
    root = root()
    user = user()

    headers = conftest.auth_user(root)
    print(root.id)
    response = client.delete(f'/users/{user.id}', headers=headers)

    assert response.json()['id'] == user.id
    assert response.status_code == 202


@pytest.mark.parametrize('root, user', [
    [user_creator.root_user, user_creator.root_user],
    [user_creator.admin_user, user_creator.admin_user],
    [user_creator.user, user_creator.user],
    [user_creator.user, user_creator.admin_user],
    [user_creator.user, user_creator.root_user]
])
def test_set_inactive_user_bad(root, user):
    root = root(username='user1')
    user = user(username='user2')

    headers = conftest.auth_user(root)
    print(root.id)
    response = client.delete(f'/users/{user.id}', headers=headers)

    assert response.json()['detail'] == "You don't have permissions"
    assert response.status_code == 403


@pytest.mark.parametrize('user', [user_creator.root_user, user_creator.admin_user])
def test_get_company_users_good(user):
    company = company_creator.company()
    user = user(company=company.id)

    headers = conftest.auth_user(user)

    response = client.get(f'/users/companies/{company.id}', headers=headers)

    assert len(response.json()) == 1
    assert response.status_code == 200


@pytest.mark.parametrize()
def test_get_company_users_bad(user):
    pass