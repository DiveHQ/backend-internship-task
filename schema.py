from pydantic import BaseModel



# API Models
class UserCreate(BaseModel):
    email: str
    password: str
    role: str


class UserUpdate(BaseModel):
    password: str


class EntryCreate(BaseModel):
    text: str
    calories: int = None


class EntryUpdate(BaseModel):
    text: str
    calories: int = None