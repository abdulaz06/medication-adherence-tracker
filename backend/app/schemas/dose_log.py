import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field


class DoseLogCreate(BaseModel):
    """Body for POST /logs/items/{item_id}"""

    scheduled_date: datetime.date
    dose_index: int = Field(ge=1, default=1)
    status: Literal["taken", "skipped"] = "taken"
    skip_reason: Optional[str] = Field(default=None, max_length=120)


class DoseLogOut(BaseModel):
    id: int
    user_id: int
    item_id: int
    scheduled_date: datetime.date
    dose_index: int
    status: str
    timestamp: datetime.datetime
    skip_reason: Optional[str]

    class Config:
        from_attributes = True


# ---------- Schedule / "today" response ----------


class ScheduleItem(BaseModel):
    """One item in the daily schedule, with completion info."""

    id: int
    name: str
    type: str
    doses_per_day: int
    notes: Optional[str]
    completed_doses: int
    expected_doses: int
    completed: bool  # True if completed_doses >= expected_doses


class DailySchedule(BaseModel):
    date: datetime.date
    items: list[ScheduleItem]


# ---------- Adherence stats ----------


class ItemAdherence(BaseModel):
    item_id: int
    item_name: str
    expected: int
    taken: int
    skipped: int
    missed: int
    adherence_pct: float


class AdherenceStats(BaseModel):
    user_id: int
    start_date: datetime.date
    end_date: datetime.date
    overall_adherence_pct: float
    items: list[ItemAdherence]
    current_streak: int
    longest_streak: int
