from pydantic import BaseModel
from typing import Optional

class ItemCreate(BaseModel):
    user_id: int
    name: str
    type: str
    doses_per_day: int = 1
    schedule_days: int = 127
    notes: Optional[str] = None
    active: bool = True

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    doses_per_day: Optional[int] = None
    schedule_days: Optional[int] = None
    notes: Optional[str] = None
    active: Optional[bool] = None

class ItemOut(BaseModel):
    id: int
    user_id: int
    name: str
    type: str
    doses_per_day: int
    schedule_days: int
    notes: Optional[str] = None
    active: bool

    class Config:
        from_attributes = True