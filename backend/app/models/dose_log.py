from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

class DoseLog(Base):
    __tablename__ = "dose_logs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id", ondelete="CASCADE"), index=True, nullable=False)

    scheduled_date: Mapped[str] = mapped_column(Date, index=True, nullable=False)
    dose_index: Mapped[int] = mapped_column(Integer, nullable=False)  # 1..doses_per_day

    status: Mapped[str] = mapped_column(String(20), nullable=False)  # "taken" | "skipped"
    timestamp: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    skip_reason: Mapped[str | None] = mapped_column(String(120), nullable=True)

    user = relationship("User", backref="dose_logs")
    item = relationship("Item", backref="dose_logs")