from pydantic import BaseModel, Field
import datetime
from typing import Optional, List, Dict


class CalorieResponse(BaseModel):
    date: datetime.date = Field(...)
    time: datetime.time = Field(...)
    text: str = Field(...)
    number_of_calories: int = Field(...)
    is_below_expected: bool = Field(...)


class Calorie(CalorieResponse):
    user_id: Optional[int]


class CalorieUpdateInput(BaseModel):
    text: Optional[str]
    number_of_calories: Optional[int]


class CalorieUpdate(CalorieUpdateInput):
    updated_at: datetime.datetime
    is_below_expected: bool = Field(...)


class CalorieEntry(BaseModel):
    text: str = Field(...)
    number_of_calories: Optional[int]

    class Config:
        orm_mode = True


class CaloriePaginatedResponse(BaseModel):
    total: int = Field(...)
    page: int = Field(...)
    size: int = Field(...)
    total_pages: int = Field(...)
    calorie_entries: List[CalorieResponse] = Field(...)
    links: Optional[Dict[str, Optional[str]]]

# class C
