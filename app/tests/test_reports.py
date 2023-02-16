import pytest

from app.tests.test_user import client
from app.tests import conftest, company_creator, user_creator, import_hashrate


api_links = ['/reports/month_day', '/reports/year_quarter_month', '/reports/year_quarter',
             '/reports/year_quarter_month_day', '/reports/quarter_month', '/reports/quarter_month_day']


@pytest.mark.parametrize('user', [
    user_creator.root_user,
    user_creator.admin_user,
    user_creator.user
])
def test_reports_good(user):
    company = import_hashrate.upload()

    user = user(company=company.id, username='TestReport', email='test_report@mail.ru')

    headers = conftest.auth_user(user)

    data = {
      "output_type": "json",
      "year": 2022,
      "month": 1,
      "quarter": 1,
      "companies": [
        1
      ]
    }

    for link in api_links:
        response = client.post(link, headers=headers, json=data)
        assert response.status_code == 200
        assert response.json().get('report')


@pytest.mark.parametrize('user, company_id, detail', [
    [user_creator.root_user, 3, 'Company does not exist'],
    [user_creator.admin_user, 1, "You don't have permissions to watch this company"],
    [user_creator.user, 1, "You don't have permissions to watch this company"]
])
def test_reports_bad(user, company_id, detail):
    company = import_hashrate.upload()
    company2 = company_creator.company(company_name='Test2Company', company_id=2)

    user = user(company=2, username='TestReport', email='testreport@mail.ru')

    headers = conftest.auth_user(user)

    data = {
      "output_type": "json",
      "year": 2022,
      "month": 1,
      "quarter": 1,
      "companies": [
        company_id
      ]
    }

    for link in api_links:
        response = client.post(link, headers=headers, json=data)
        assert response.status_code == 403
        assert response.json()['detail'] == detail

