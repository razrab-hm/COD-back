from pydantic import BaseModel


class BaseModel(BaseModel):
    class Config:
        orm_mode = True


