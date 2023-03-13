from datetime import date

from pydantic import BaseModel


class HashrateBase(BaseModel):
    date: date
    average: int
    hash: int
    company_id: int


class Hashrate(BaseModel):
    id: int
    date: date
    average: float
    hash: float
    company_id: int

    class Config:
        orm_mode = True
