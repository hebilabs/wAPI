from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    fullname: str = Field(..., description="The full name of the user", example="John Doe")
    email: EmailStr = Field(..., description="The email address of the user", example="user@example.com")
    password: str = Field(..., description="The password of the user", example="password")
    address: str = Field(..., description="The address of the user", example="123 Main St, Anytown, USA")
    is_admin: int = Field(..., description="The admin status of the user", example=0)


class UserResponse(BaseModel):
    id: int
    fullname: str = Field(..., description="The full name of the user", example="John Doe")
    email: EmailStr = Field(..., description="The email address of the user", example="user@example.com")
    password: str = Field(..., description="The password of the user", example="password")
    address: str = Field(..., description="The address of the user", example="123 Main St, Anytown, USA")
    is_admin: int = Field(..., description="The admin status of the user", example=0)
