from pydantic import BaseModel


class PermissionBase(BaseModel):
    permission_name: str


class Permission(BaseModel):
    id: int
    permission_name: str

    class Config:
        orm_mode = True



