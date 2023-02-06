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
        'hash': 40.0,
        'company_id': company.id
    }

    response = client.post('/hashrates', headers=headers, json=data)

    res_data = response.json()
    res_data.pop('id')
    res_data.pop('user_id')

    assert response.status_code == 201
    assert res_data == data


@pytest.mark.parametrize('user, company_id, status_code, detail', [
    [user_creator.user, 1, 406, "You don't have permissions"],
    [user_creator.admin_user, 2, 403, "Company does not exist"],
    [user_creator.root_user, 2, 403, "Company does not exist"]
])
def test_create_hashrate_bad(user, company_id, status_code, detail):
    company = company_creator.company()
    user = user(company=company.id)
    headers = conftest.auth_user(user)

    data = {
        'date': '2023-02-06',
        'average': 20.0,
        'hash': 40.0,
        'company_id': company_id
    }

    response = client.post('/hashrates', headers=headers, json=data)

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

    response = client.post('/hashrates', headers=headers, json=data)

    assert response.status_code == 406
    assert response.json()['detail'] == "You don't have permissions"


