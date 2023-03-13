from pydantic import BaseModel


class BaseModel(BaseModel):
    class Config:
        orm_mode = True


class CompanyCreate(BaseModel):
    id: int
    title: str = None
    contact_fio: str = None
    contact_email: str = None
    contact_phone: str = None
    img_logo: str = None
    description: str = None
    inactive: bool = False


class CompanyUpdate(BaseModel):
    id: int
    title: str = None
    contact_fio: str = None
    contact_email: str = None
    contact_phone: str = None
    img_logo: str = None
    description: str = None
    inactive: bool = False


class CompaniesGet(BaseModel):
    id: int
    title: str = None
    contact_fio: str = None
    contact_email: str = None
    contact_phone: str = None
    img_logo: str = None
    description: str = None
    inactive: bool = False


class CompanyGetId(BaseModel):
    id: int
    title: str = None
    contact_fio: str = None
    contact_email: str = None
    contact_phone: str = None
    img_logo: str = None
    description: str = None
    inactive: bool = False



