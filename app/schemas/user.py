from pydantic import BaseModel


class UserCreate(BaseModel):
    fullname: str
    email: str
    password: str
    address: str
    is_admin: int = 0  # mass assignment


class UserResponse(BaseModel):
    id: int
    fullname: str
    email: str
    password: str   # data exposure
    address: str
    is_admin: int
