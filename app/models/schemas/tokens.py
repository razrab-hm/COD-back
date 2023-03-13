from pydantic import BaseModel


class BaseModel(BaseModel):
    class Config:
        orm_mode = True


class TokenCreate(BaseModel):
    access_token: str
    refresh_token: str


class TokenValid(BaseModel):
    message: str
    role: str
