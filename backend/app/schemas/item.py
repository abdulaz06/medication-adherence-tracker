from pydantic import BaseModel, Field
from typing import Optional, Literal


class ItemBase(BaseModel):
    user_id: int
    name: str = Field(min_length=1, max_length=120)
    type: Literal["medication", "supplement"]
    doses_per_day: int = Field(ge=1, le=24, default=1)
    schedule_days: int = Field(ge=0, le=127, default=127)
    notes: Optional[str] = Field(default=None, max_length=255)
    active: bool = True


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    # all optional for PATCH
    name: Optional[str] = Field(default=None, min_length=1, max_length=120)
    type: Optional[Literal["medication", "supplement"]] = None
    doses_per_day: Optional[int] = Field(default=None, ge=1, le=24)
    schedule_days: Optional[int] = Field(default=None, ge=0, le=127)
    notes: Optional[str] = Field(default=None, max_length=255)
    active: Optional[bool] = None


class ItemOut(ItemBase):
    id: int

    class Config:
        from_attributes = True