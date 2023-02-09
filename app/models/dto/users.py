from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    password: str


class UserCreate(UserBase):
    email: str
    first_name: str = None
    last_name: str = None
    description: str = ''


class UserCreateAdmin(UserBase):
    email: str
    first_name: str = None
    last_name: str = None
    companies_id: list[int]


class UserUpdate(UserBase):
    id: int
    email: str = None
    password: str = None
    role: str = None
    username: str = None
    first_name: str = None
    last_name: str = None
    inactive: str = None


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

