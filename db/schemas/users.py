from pydantic import BaseModel
from pydantic.schema import Optional


class UserBase(BaseModel):
    email: str
    password: str


class UserCreate(UserBase):
    pass
    # company_id: int
    # permission_id: int


class Settings(BaseModel):
    authjwt_secret_key: str = "secret"


class TokenBase(BaseModel):
    access_token: str


class User(BaseModel):
    permission_id: Optional[int]
    company_id: Optional[int]
    id: int
    email: str
    hash_password: str

    class Config:
        orm_mode = True

