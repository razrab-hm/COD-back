from pydantic import BaseModel
from pydantic.schema import Optional


class UserBase(BaseModel):
    username: str
    password: str


class UserCreate(UserBase):
    email: str
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
    username: str

    class Config:
        orm_mode = True

