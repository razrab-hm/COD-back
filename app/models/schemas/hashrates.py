from datetime import date

from pydantic import BaseModel


class BaseModel(BaseModel):
    class Config:
        orm_mode = True


class HashrateCreate(BaseModel):
    id: int
    date: date
    average: float
    hash: float
    company_id: int
    user_id: int = None


class HashrateImport(BaseModel):
    status: str = 'New'
