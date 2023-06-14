from pydantic import BaseModel, Field
from typing import Any

class APIResponse(BaseModel):
    data: Any = Field(...)
    errors: dict = Field(...)
    status_code: int = Field(...)