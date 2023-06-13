from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict
from src.db.models import Role
import datetime


class User(BaseModel):
    email: EmailStr = Field(...)
    first_name: str = Field(..., min_length=2)
    last_name: str = Field(..., min_length=2)
    password: str = Field(..., min_length=5)
    password_confirmation: str = Field(..., min_length=5)
    role: Optional[Role]

class UserResponse(BaseModel):
    email: Optional[EmailStr] = Field(...)
    first_name: Optional[str] = Field(...)
    last_name: Optional[str] = Field(...)
    role: Role = Field(...)
    expected_calories: int = Field(...)

class UserPaginatedResponse(BaseModel):
    total: int = Field(...)
    page: int = Field(...)
    size: int = Field(...)
    total_pages: int = Field(...)
    users_response: List[UserResponse] = Field(...)
    links: Optional[Dict[str, Optional[str]]]


class UserWithRole(User):
    role: Role = Field(...)





class UserUpdateResponse(UserResponse):
    updated_at: datetime.datetime = Field(...)


class Token(BaseModel):
    token: str = Field(...)
    token_type: str = Field(...)
    exp: float = Field(...)


class TokenData(BaseModel):
    id: Optional[str] = Field(default=None)


class TotalUsers(BaseModel):
    total: int = Field(...)
    data: List[UserResponse] = Field(...)


class UserUpdate(BaseModel):
    email: Optional[EmailStr]
    first_name: Optional[str]
    last_name: Optional[str]
    updated_at: Optional[datetime.datetime]
    role: Optional[Role]
    expected_calories: Optional[int]


class AdminUserUpdate(UserUpdate):
    role: Optional[Role]
