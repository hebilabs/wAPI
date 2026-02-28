from pydantic import BaseModel, EmailStr, Field


class LoginSchema(BaseModel):
    email: EmailStr = Field(..., description="The email address of the user", example="user@example.com")
    password: str = Field(..., description="The password of the user", example="password")