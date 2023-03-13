import pytest

from app.tests.test_user import client
from app.tests import conftest, company_creator
from app.tests import user_creator


def test_create_company_good():
    user = user_creator.root_user()
    headers = conftest.auth_user(user)
    data = {
              "title": "TestCompany",
              "contact_fio": "TestFIO",
              "contact_email": "TestContactEmail@mail.ru",
              "contact_phone": "+7952111111",
              "description": "test description"
            }
    response = client.post('/api/companies', headers=headers, json=data)

    assert response.status_code == 201
    assert response.json()['title'] == data['title']
    assert response.json()['contact_fio'] == data['contact_fio']


def test_create_company_bad_username():
    user = user_creator.root_user()
    headers = conftest.auth_user(user)
    data = {
              "title": "TestCompany<div>",
              "contact_fio": "TestFIO",
              "contact_email": "TestContactEmail@mail.ru",
              "contact_phone": "+7952111111",
              "description": "test description"
            }
    response = client.post('/api/companies', headers=headers, json=data)

    assert response.status_code == 406
    assert response.json()['detail'] == 'Symbols in your fields not ascii symbols or numerics'


def test_create_company_bad_phone():
    user = user_creator.root_user()
    headers = conftest.auth_user(user)
    data = {
              "title": "TestCompany",
              "contact_fio": "TestFIO",
              "contact_email": "TestContactEmail@mail.ru",
              "contact_phone": "+sd7952111111",
              "description": "test description"
            }
    response = client.post('/api/companies', headers=headers, json=data)

    assert response.status_code == 406
    assert response.json()['detail'] == 'Phone incorrect'


@pytest.mark.parametrize('user', [user_creator.admin_user, user_creator.user])
def test_create_company_bad(user):
    user = user()
    headers = conftest.auth_user(user)
    data = {
              "title": "TestCompany",
              "contact_fio": "TestFIO",
              "contact_email": "TestContactEmail",
              "contact_phone": "+7952111111",
              "img_logo": "test_logo_path",
              "description": "test description"
            }
    response = client.post('/api/companies', headers=headers, json=data)

    assert response.status_code == 406
    assert response.json()['detail'] == "You don't have permissions"


def test_update_company_good():
    user = user_creator.root_user()
    headers = conftest.auth_user(user)
    company = company_creator.company()
    data = {'id': company.id,
            'title': 'TestTitle',
            'contact_fio': 'TestFIO',
            'contact_email': 'TestEMAIL@mail.ru',
            'contact_phone': '+799999999',
            'description': 'TEST DESCRIPTION'
            }
    response = client.put('/api/companies', headers=headers, json=data)

    assert response.status_code == 200
    assert response.json()['title'] != company.title
    assert response.json()['contact_fio'] != company.contact_fio
    assert response.json()['contact_email'] != company.contact_email
    assert response.json()['contact_phone'] != company.contact_phone
    assert response.json()['description'] != company.description
    assert response.json()['id'] == company.id


@pytest.mark.parametrize('user', [user_creator.user, user_creator.admin_user])
def test_update_company_bad(user):
    user = user()
    headers = conftest.auth_user(user)
    company = company_creator.company()
    data = {'id': company.id,
            'title': 'TestTitle',
            'contact_fio': 'TestFIO',
            'contact_email': 'TestEMAIL',
            'contact_phone': 'TestPHONE',
            'img_logo': 'testLOGO',
            'description': 'TEST DESCRIPTION'
            }
    response = client.put('/api/companies', headers=headers, json=data)

    assert response.status_code == 406
    assert response.json()['detail'] == "You don't have permissions"


@pytest.mark.parametrize('user, company_len', [[user_creator.root_user, 2],
                                               [user_creator.admin_user, 1],
                                               [user_creator.user, 0]])
def test_get_companies_good(user, company_len):
    company = company_creator.company()
    company2 = company_creator.company(company_id=2, company_name='Test2Company')
    user = user(company=company.id)
    headers = conftest.auth_user(user)

    response = client.get('/api/companies', headers=headers)

    assert response.status_code == 200
    assert len(response.json()) == company_len


@pytest.mark.parametrize('user', [user_creator.admin_user, user_creator.root_user])
def test_get_company_by_id_good(user):
    company = company_creator.company()
    user = user(company=company.id)
    headers = conftest.auth_user(user)

    response = client.get(f'/api/companies/company/{company.id}', headers=headers)

    assert response.status_code == 200
    assert response.json()['id'] == company.id


@pytest.mark.parametrize('user', [user_creator.admin_user, user_creator.user])
def test_get_company_by_id_bad(user):
    company = company_creator.company()
    company2 = company_creator.company(company_name="Test2Company", company_id=2)
    user = user(company=company.id)
    headers = conftest.auth_user(user)

    response = client.get(f'/api/companies/company/{company2.id}', headers=headers)

    assert response.status_code == 406
    assert response.json()['detail'] == "You don't have permissions"


def test_delete_company_good():
    company = company_creator.company()
    root = user_creator.root_user(company=company.id)
    headers = conftest.auth_user(root)

    response = client.delete(f'/api/companies/{company.id}', headers=headers)

    assert response.status_code == 205
    assert response.json()['id'] == company.id


@pytest.mark.parametrize('user, company_id, status_code, detail', [
    [user_creator.user, 1, 406, "You don't have permissions"],
    [user_creator.admin_user, 1, 406, "You don't have permissions"],
    [user_creator.root_user, 2, 403, "Company does not exist"],
])
def test_delete_company_bad(user, company_id, status_code, detail):
    company = company_creator.company()
    user = user(company=company.id)
    headers = conftest.auth_user(user)

    response = client.delete(f'/api/companies/{company_id}', headers=headers)

    assert response.status_code == status_code
    assert response.json()['detail'] == detail



