import pytest

from app.tests.test_user import client
from app.tests import conftest, company_creator, user_creator


@pytest.mark.parametrize('user', [user_creator.root_user, user_creator.admin_user])
def test_create_hashrate_good(user):
    company = company_creator.company()
    root = user(company=company.id)
    headers = conftest.auth_user(root)

    data = {
        'date': '2023-02-06',
        'average': 20.0,
        'company_id': company.id
    }

    response = client.post('/api/hashrates', headers=headers, json=data)

    res_data = response.json()

    assert response.status_code == 201
    assert res_data[0]['date'] == data['date']

    response = client.post(f'/api/hashrates/import/{company.id}/save', headers=headers, json=res_data)

    assert response.json()[0]['status'] == 'new'

    response = client.post(f'/api/hashrates/import/{company.id}/save', headers=headers, json=res_data)

    assert response.json()[0]['status'] == 'updated'


@pytest.mark.parametrize('user, company_id, status_code, detail', [
    [user_creator.user, 1, 406, "You don't have permissions"],
    [user_creator.admin_user, 2, 403, "Company does not exist"],
    [user_creator.root_user, 2, 403, "Company does not exist"],
    [user_creator.admin_user, 2, 406, "You don't have permissions"]
])
def test_create_hashrate_bad(user, company_id, status_code, detail):
    company = company_creator.company()
    user = user(company=company.id)
    if user.role == 'admin' and status_code == 406:
        company2 = company_creator.company("Test2Company", 2)
    headers = conftest.auth_user(user)

    data = {
        'date': '2023-02-06',
        'average': 20.0,
        'hash': 40.0,
        'company_id': company_id
    }

    response = client.post('/api/hashrates', headers=headers, json=data)

    assert response.status_code == status_code
    assert response.json()['detail'] == detail


@pytest.mark.parametrize('user', [user_creator.admin_user])
def test_create_hashrate_admin_not_in_company_bad(user):
    company = company_creator.company()
    company2 = company_creator.company(company_name='Test2Company', company_id=2)
    user = user(company=company.id)
    headers = conftest.auth_user(user)

    data = {
        'date': '2023-02-06',
        'average': 20.0,
        'hash': 40.0,
        'company_id': 2
    }

    response = client.post('/api/hashrates', headers=headers, json=data)

    assert response.status_code == 406
    assert response.json()['detail'] == "You don't have permissions"


@pytest.mark.parametrize('user', [
    user_creator.root_user, user_creator.admin_user
])
def test_import_hashrate_good(user):
    company = company_creator.company()
    user = user(company=company.id)
    headers = conftest.auth_user(user)

    file = {'file': open('test_hr.xls', 'rb')}

    response = client.post(f'/api/hashrates/import/{company.id}', headers=headers, files=file)

    assert response.json()[0]['status'] == 'new'


@pytest.mark.parametrize('user, company_id', [
    [user_creator.user, 1],
    [user_creator.admin_user, 2]
])
def test_import_hashrate_bad(user, company_id):
    company = company_creator.company()
    company2 = company_creator.company(company_name='Test2Company', company_id=2)
    user = user(company=company.id)
    headers = conftest.auth_user(user)

    file = {'file': open('test_hr.xls', 'rb')}

    response = client.post(f'/api/hashrates/import/{company_id}', headers=headers, files=file)

    assert response.status_code == 406
    assert response.json()['detail'] == "You don't have permissions"


def test_import_hashrate_company_bad():
    company = company_creator.company()
    user = user_creator.user(company=company.id)
    headers = conftest.auth_user(user)

    file = {'file': open('test_hr.xls', 'rb')}

    response = client.post(f'/api/hashrates/import/2', headers=headers, files=file)

    assert response.status_code == 403
    assert response.json()['detail'] == "Company does not exist"


# def test_update_hashrate_good():
#     company = company_creator.company()
#     user = user_creator.admin_user(company=company.id)
#     headers = conftest.auth_user(user)
#
#     data = {
#         'date': '2023-02-06',
#         'average': 20.0,
#         'company_id': company.id
#     }
#
#     response = client.post('/api/hashrates', headers=headers, json=data)
#
#     res_data = response.json()
#
#     assert response.status_code == 201
#     assert res_data[0]['date'] == data['date']
#
#     response = client.post(f'/api/hashrates/import/{company.id}/save', headers=headers, json=res_data)
#
#     assert response.json()[0]['status'] == 'new'
#
#     response = client.get(f'/api/hashrates/company/{company.id}', headers=headers)
#
#     assert response.json()[0]['average'] == 20.0
#
#     update_data = {
#         "id": response.json()[0]['id'],
#         "average": 30.0
#     }
#
#     response = client.put('/api/hashrates/', headers=headers, json=update_data)
#
#     assert response.json()['average'] == 30.0
#
#     response = client.get(f'/api/hashrates/company/{company.id}', headers=headers)
#
#     assert response.json()[0]['average'] == 30.0


# @pytest.mark.parametrize('user', [user_creator.admin_user, user_creator.root_user])
# def test_delete_hashrate_good(user):
#     company = company_creator.company()
#     user = user(company=company.id)
#     headers = conftest.auth_user(user)
#
#     file = {'file': open('test_hr.xls', 'rb')}
#
#     response = client.post(f'/api/hashrates/import/{company.id}', headers=headers, files=file)
#
#     assert response.json()[0]['status'] == 'new'
#
#     response = client.get(f'/api/hashrates/company/{company.id}', headers=headers)
#
#     assert response.json()[0]['date'] == '2021-09-30'
#
#     response = client.delete(f'/api/hashrates/company/{company.id}?from_date=2021-09-30&to_date=2022-09-30', headers=headers)
#
#     assert response.json()['detail'] == 'success, deleted 366 values.'
#
#     response = client.get(f'/api/hashrates/company/{company.id}', headers=headers)
#
#     assert response.json()[0]['date'] == '2021-09-29'


