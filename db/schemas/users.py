from pydantic import BaseModel
from pydantic.schema import Optional


class UserBase(BaseModel):
    email: str
    password: str


class UserCreate(UserBase):
    role: str = 'manager'
    company_id: int = None
    # company_id: int
    # permission_id: int


class UserUpdate(UserBase):
    id: int
    email: str = None
    password: str = None
    role: str = None
    company_id: int = None


class Settings(BaseModel):
    authjwt_secret_key: str = "secret"


class TokenBase(BaseModel):
    access_token: str


class User(BaseModel):
    company_id: Optional[int]
    role: str
    id: int
    email: str
    hash_password: str
    inactive: bool = False

    class Config:
        orm_mode = True

