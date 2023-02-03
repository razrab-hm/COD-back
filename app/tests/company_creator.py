from app.models.db import users, companies, auth, hashrates
from app.app import db as core_db


def company(company_name='TestCompany', company_id=1):
    db = core_db.get_core_db()

    db_user = companies.Company(id=company_name,
                                username=company_name,
                                email='user@mail.ru',
                                hash_password=hashlib.md5('qwerty'.encode('utf-8')).hexdigest(),
                                role='manager', inactive=False)

    if company:
        user_company = users.UserCompany(company_id=1, user_id=db_user.id)
        db.add(user_company)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db.close()
    return db_user