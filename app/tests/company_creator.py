from app.models.db import users, companies, auth, hashrates
from app.app import db as core_db


def company(company_name='TestCompany', company_id=1):
    db = core_db.get_core_db()

    db_company = companies.Company(id=company_id,
                                   title=company_name)

    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    db.close()
    return db_company

