

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from db.models import Role

class User(BaseModel):
    email: EmailStr = Field(...)
    first_name: str = Field(...)
    last_name: str = Field(...)
    password: str = Field(...)
    password_confirmation: str = Field(...)

    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    id: int = Field(...)
    email: Optional[EmailStr] = Field(...)
    first_name: Optional[str] = Field(...)
    last_name: Optional[str] = Field(...)
    role: Role = Field(...)
    expected_calories: int = Field(...)

class Token(BaseModel):
    token: str = Field(...)
    token_type: str = Field(...)

class TokenData(BaseModel):
    id: Optional[str] = Field(default=None)