from pydantic import BaseModel


class CompanyBase(BaseModel):
    title: str
    contact_fio: str
    contact_email: str
    contact_phone: str
    img_logo: str
    description: str


class CompanyUpdate(BaseModel):
    id: int
    title: str = None
    contact_fio: str = None
    contact_email: str = None
    contact_phone: str = None
    img_logo: str = None
    description: str = None


class CompanyRead(BaseModel):
    id: int


class Company(BaseModel):
    id: int
    title: str
    contact_fio: str
    contact_email: str
    contact_phone: str
    img_logo: str
    description: str
    inactive: bool

    class Config:
        orm_mode = True



