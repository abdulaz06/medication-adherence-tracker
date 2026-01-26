from pydantic import BaseModel
from datetime import date
from typing import Optional

class DoseLogCreate(BaseModel):
    item_id: int
    scheduled_date: date
    dose_index: int
    status: str  # "taken" or "skipped"
    skip_reason: Optional[str] = None

class DoseLogOut(BaseModel):
    id: int
    user_id: int
    item_id: int
    scheduled_date: date
    dose_index: int
    status: str
    skip_reason: Optional[str]

    class Config:
        from_attributes = True