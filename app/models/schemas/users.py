from pydantic import BaseModel


class BaseModel(BaseModel):
    class Config:
        orm_mode = True


class UserRegister(BaseModel):
    username: str
    role: str = 'manager'


class UserLogin(BaseModel):
    access_token: str
    refresh_token: str
    role: str = 'manager'
    message: str = None


class UserLogout(BaseModel):
    status: str = 'ok'


class UserUpdate(BaseModel):
    id: int
    email: str = None
    hash_password: str = None
    role: str = None
    inactive: bool = False
    username: str = None
    first_name: str = None
    last_name: str = None


class UserMe(BaseModel):
    username: str
    role: str = 'manager'


class UsersGetId(BaseModel):
    id: int


class UserGetId(BaseModel):
    id: int
    email: str = None
    hash_password: str = None
    role: str = None
    inactive: bool = False
    username: str = None
    first_name: str = None
    last_name: str = None
    description: str = None


class UserCompany(BaseModel):
    user_id: int
    company_id: int


class UserUpdateCompanies(BaseModel):
    updated_companies: list[UserCompany]

