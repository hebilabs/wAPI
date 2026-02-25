from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    is_admin: bool = False  #mass assignment

class UserResponse(BaseModel):
    id: int
    username: str
    password: str   #data exposure
    is_admin: bool