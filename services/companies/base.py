from sqlalchemy.orm import Session

from services.companies import schemas, models


def create_company(db: Session, company: schemas.CompanyBase):
    db_company = models.Company(name=company.name, contact_name=company.contact_name, contact_email=company.contact_email)
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company


def get_company_by_id(db: Session, company_id: int):
    return db.query(models.Company).filter(models.Company.id == company_id).first()

