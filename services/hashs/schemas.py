from datetime import date

from pydantic import BaseModel


class HashBase(BaseModel):
    date: date
    average: int
    hash: int
    company_id: int


class Hash(BaseModel):
    id: int
    date: date
    average: float
    hash: float
    company_id: int

    class Config:
        orm_mode = True
