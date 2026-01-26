from pydantic import BaseModel
from typing import Optional

class ItemCreate(BaseModel):
    name: str
    type: str
    doses_per_day: int = 1
    schedule_days: int = 127
    notes: Optional[str] = None
    active: bool = True

class ItemOut(ItemCreate):
    id: int
    user_id: int

    class Config:
        from_attributes = True