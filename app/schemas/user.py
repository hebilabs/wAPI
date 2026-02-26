from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    password: str
    is_admin: int = 0  # mass assignment


class UserResponse(BaseModel):
    id: int
    email: str
    password: str   # data exposure
    is_admin: int
