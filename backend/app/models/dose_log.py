import datetime

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class DoseLog(Base):
    __tablename__ = "dose_logs"

    # Prevent duplicate logs for the same item/date/dose_index
    __table_args__ = (
        UniqueConstraint("item_id", "scheduled_date", "dose_index", name="uq_item_date_dose"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    item_id: Mapped[int] = mapped_column(
        ForeignKey("items.id", ondelete="CASCADE"), index=True, nullable=False
    )

    scheduled_date: Mapped[datetime.date] = mapped_column(Date, index=True, nullable=False)
    dose_index: Mapped[int] = mapped_column(Integer, nullable=False, default=1)  # 1..doses_per_day

    status: Mapped[str] = mapped_column(String(20), nullable=False)  # "taken" | "skipped"
    timestamp: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    skip_reason: Mapped[str | None] = mapped_column(String(120), nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="dose_logs")
    item: Mapped["Item"] = relationship("Item", back_populates="dose_logs")
