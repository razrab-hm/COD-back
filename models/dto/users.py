from pydantic import BaseModel
from pydantic.schema import Optional


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str
    # role: str = 'manager'
    # company_id: int
    # permission_id: int


class UserUpdate(UserBase):
    id: int
    email: str = None
    password: str = None
    role: str = None


class UserRead(BaseModel):
    id: int


class Settings(BaseModel):
    authjwt_secret_key: str = "secret"


class TokenBase(BaseModel):
    access_token: str


class Token(BaseModel):
    access_token: str
    refresh_token: str


class User(BaseModel):
    role: str
    id: int
    email: str
    hash_password: str
    inactive: bool = False

    class Config:
        orm_mode = True
