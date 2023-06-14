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


class UserRes(BaseModel):
    email: Optional[EmailStr] = Field(...)
    first_name: Optional[str] = Field(...)
    last_name: Optional[str] = Field(...)
    role: Role = Field(...)
    expected_calories: int = Field(...)

class UserResponse(BaseModel):
    data: UserRes = Field(...)
    errors: list = Field(...)
    status_code: int = Field(...)


class UserPaginate(BaseModel):
    total: int = Field(...)
    page: int = Field(...)
    size: int = Field(...)
    total_pages: int = Field(...)
    users_response: List[UserRes] = Field(...)
    links: Optional[Dict[str, Optional[str]]]

class UserPaginatedResponse(BaseModel):
    data: UserPaginate = Field(...)
    errors: list = Field(...)
    status_code: int = Field(...)


class UserUpdate(UserRes):
    updated_at: datetime.datetime = Field(...)

class UserUpdateResponse(BaseModel):
    data: UserUpdate = Field(...)
    errors: list = Field(...)
    status_code: int = Field(...)

class Token(BaseModel):
    token: str = Field(...)
    token_type: str = Field(...)
    exp: float = Field(...)

class TokenResponse(BaseModel):
    data: Token = Field(...)
    errors: list = Field(...)
    status_code: int = Field(...)


class TokenData(BaseModel):
    id: Optional[str] = Field(default=None)

class UserUpdate(BaseModel):
    email: Optional[EmailStr]
    first_name: Optional[str]
    last_name: Optional[str]
    updated_at: Optional[datetime.datetime]
    role: Optional[Role]
    expected_calories: Optional[int]

