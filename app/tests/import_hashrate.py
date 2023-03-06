from app.tests import company_creator, user_creator, conftest
from app.tests.test_user import client


def upload(company_id=1):
    company = company_creator.company(company_id=company_id)
    user = user_creator.root_user(company=company.id)
    headers = conftest.auth_user(user)

    file = {'file': open('test_hr.xls', 'rb')}

    response = client.post(f'/api/hashrates/import/{company.id}', headers=headers, files=file)

    return company
