from pydantic import BaseModel


class CompanyBase(BaseModel):
    name: str
    contact_name: str
    contact_email: str


class Company(BaseModel):
    id: int
    name: str
    contact_name: str
    contact_email: str

    class Config:
        orm_mode = True
