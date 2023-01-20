from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    password: str


class UserCreate(UserBase):
    company_id: int = 0
    permission_id: int = 3


class Settings(BaseModel):
    authjwt_secret_key: str = "secret"


class TokenBase(BaseModel):
    access_token: str


class User(BaseModel):
    permission_id: int
    company_id: int
    id: int
    email: str
    hash_password: str

    class Config:
        orm_mode = True

