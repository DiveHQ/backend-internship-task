

from pydantic import BaseModel, Field
import datetime
from typing import Optional, List, Dict

class Calorie(BaseModel):
    date: datetime.date = Field(...)
    time: datetime.time = Field(...)
    text: str = Field(...)
    number_of_calories: int = Field(...)
    user_id: int = Field(...)
    is_below_expected: bool = Field(...)

    # class Config:
    #     orm_mode = True

class CalorieResponse(Calorie):
    id: int = Field(...)

class CalorieUpdate(BaseModel):
    text: Optional[str]
    number_of_calories: Optional[int]
    is_below_expected: Optional[bool]
    updated_at: Optional[datetime.datetime]

class CalorieEntry(BaseModel):
    text: str = Field(...)
    number_of_calories: Optional[int]

    class Config:
        orm_mode = True

class CalorieEntryResponse(BaseModel):
    total: int = Field(...)
    data: List[Calorie]

    class Config:
        orm_mode = True

class CaloriePaginatedResponse(BaseModel):
    total: int = Field(...)
    page: int = Field(...)
    size: int = Field(...)
    pages: int = Field(...)
    calorie_entries: List[Calorie] = Field(...)
    links: Optional[Dict[str, Optional[str]]]

class CalorieEntryResponse(BaseModel):
    total: int = Field(...)
    data: Calorie
