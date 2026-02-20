import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import and_, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.dose_log import DoseLog
from app.models.item import Item
from app.models.user import User
from app.schemas.dose_log import (
    AdherenceStats,
    DailySchedule,
    DoseLogCreate,
    DoseLogOut,
    ItemAdherence,
    ScheduleItem,
)

router = APIRouter(prefix="/logs", tags=["logs"])

# ---------- Bitmask helpers ----------
# Mon=1  Tue=2  Wed=4  Thu=8  Fri=16  Sat=32  Sun=64
# Python weekday(): Mon=0 .. Sun=6
WEEKDAY_BITS = {0: 1, 1: 2, 2: 4, 3: 8, 4: 16, 5: 32, 6: 64}


def _is_scheduled(schedule_days: int, target_date: datetime.date) -> bool:
    bit = WEEKDAY_BITS[target_date.weekday()]
    return bool(schedule_days & bit)


def _verify_user(user_id: int, db: Session) -> None:
    if not db.get(User, user_id):
        raise HTTPException(status_code=404, detail="User not found")


# ================================================================
# STEP A — Dose log CRUD
# ================================================================


@router.post(
    "/items/{item_id}",
    response_model=DoseLogOut,
    status_code=status.HTTP_201_CREATED,
)
def create_dose_log(
    item_id: int,
    payload: DoseLogCreate,
    user_id: int = Query(..., description="Owner user_id (will come from JWT later)"),
    db: Session = Depends(get_db),
):
    """Mark a dose as taken or skipped for a given item, date, and dose_index."""
    # Validate item exists and belongs to user
    item = db.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if item.user_id != user_id:
        raise HTTPException(status_code=403, detail="Item does not belong to this user")

    # Validate dose_index within range
    if payload.dose_index > item.doses_per_day:
        raise HTTPException(
            status_code=422,
            detail=f"dose_index {payload.dose_index} exceeds item's doses_per_day ({item.doses_per_day})",
        )

    # Validate skip_reason only provided when status is skipped
    if payload.status == "taken" and payload.skip_reason:
        raise HTTPException(status_code=422, detail="skip_reason is only valid when status is 'skipped'")

    log = DoseLog(
        user_id=user_id,
        item_id=item_id,
        scheduled_date=payload.scheduled_date,
        dose_index=payload.dose_index,
        status=payload.status,
        skip_reason=payload.skip_reason,
    )

    try:
        db.add(log)
        db.commit()
        db.refresh(log)
    except IntegrityError:
        db.rollback()
        # Duplicate — return existing log
        existing = (
            db.query(DoseLog)
            .filter(
                DoseLog.item_id == item_id,
                DoseLog.scheduled_date == payload.scheduled_date,
                DoseLog.dose_index == payload.dose_index,
            )
            .first()
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Log already exists for this item/date/dose_index",
            )
        raise  # unexpected integrity error

    return log


@router.get("/by-user/{user_id}", response_model=list[DoseLogOut])
def list_logs_for_user(
    user_id: int,
    start: Optional[datetime.date] = Query(None, description="Start date (inclusive)"),
    end: Optional[datetime.date] = Query(None, description="End date (inclusive)"),
    item_id: Optional[int] = Query(None, description="Filter by specific item"),
    db: Session = Depends(get_db),
):
    """Fetch all dose logs for a user, optionally filtered by date range and item."""
    _verify_user(user_id, db)

    query = db.query(DoseLog).filter(DoseLog.user_id == user_id)

    if start:
        query = query.filter(DoseLog.scheduled_date >= start)
    if end:
        query = query.filter(DoseLog.scheduled_date <= end)
    if item_id:
        query = query.filter(DoseLog.item_id == item_id)

    return query.order_by(DoseLog.scheduled_date.desc(), DoseLog.timestamp.desc()).all()


@router.delete("/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_dose_log(log_id: int, db: Session = Depends(get_db)):
    """Remove a log entry (undo a mark)."""
    log = db.get(DoseLog, log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    db.delete(log)
    db.commit()
    return


@router.patch("/{log_id}", response_model=DoseLogOut)
def update_dose_log(
    log_id: int,
    status_val: Optional[str] = Query(None, alias="status", pattern="^(taken|skipped)$"),
    skip_reason: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """Update a log's status (e.g. change from taken to skipped)."""
    log = db.get(DoseLog, log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")

    if status_val is not None:
        log.status = status_val
    if skip_reason is not None:
        log.skip_reason = skip_reason if skip_reason else None
    if log.status == "taken":
        log.skip_reason = None  # clear skip_reason when marking taken

    db.commit()
    db.refresh(log)
    return log


# ================================================================
# STEP B — Today's schedule endpoint
# ================================================================


@router.get("/schedule/{user_id}", response_model=DailySchedule)
def get_daily_schedule(
    user_id: int,
    date: Optional[datetime.date] = Query(None, description="Date (defaults to today)"),
    db: Session = Depends(get_db),
):
    """
    Returns the list of active items scheduled for the given day,
    along with completion status from dose_logs.
    """
    _verify_user(user_id, db)

    target_date = date or datetime.date.today()

    # Fetch all active items for this user
    items = (
        db.query(Item)
        .filter(Item.user_id == user_id, Item.active == True)  # noqa: E712
        .all()
    )

    # Filter to items scheduled for this day of the week
    scheduled_items = [i for i in items if _is_scheduled(i.schedule_days, target_date)]

    # Fetch logs for this date in one query
    logs = (
        db.query(DoseLog)
        .filter(
            DoseLog.user_id == user_id,
            DoseLog.scheduled_date == target_date,
        )
        .all()
    )

    # Index logs by item_id
    logs_by_item: dict[int, list[DoseLog]] = {}
    for log in logs:
        logs_by_item.setdefault(log.item_id, []).append(log)

    result_items = []
    for item in scheduled_items:
        item_logs = logs_by_item.get(item.id, [])
        taken_count = sum(1 for l in item_logs if l.status == "taken")
        completed_doses = len(item_logs)  # taken + skipped both count as "addressed"

        result_items.append(
            ScheduleItem(
                id=item.id,
                name=item.name,
                type=item.type,
                doses_per_day=item.doses_per_day,
                notes=item.notes,
                completed_doses=taken_count,
                expected_doses=item.doses_per_day,
                completed=taken_count >= item.doses_per_day,
            )
        )

    return DailySchedule(date=target_date, items=result_items)


# ================================================================
# Adherence stats endpoint
# ================================================================


@router.get("/stats/{user_id}", response_model=AdherenceStats)
def get_adherence_stats(
    user_id: int,
    days: int = Query(7, ge=1, le=365, description="Number of past days to compute stats over"),
    db: Session = Depends(get_db),
):
    """
    Compute adherence statistics for a user over the last N days.
    Returns per-item breakdown, overall %, and streak info.
    """
    _verify_user(user_id, db)

    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=days - 1)

    # Get all active items
    items = (
        db.query(Item)
        .filter(Item.user_id == user_id, Item.active == True)  # noqa: E712
        .all()
    )

    # Get all logs in range
    logs = (
        db.query(DoseLog)
        .filter(
            DoseLog.user_id == user_id,
            DoseLog.scheduled_date >= start_date,
            DoseLog.scheduled_date <= end_date,
        )
        .all()
    )

    # Index logs: (item_id, date) -> list of logs
    log_index: dict[tuple[int, datetime.date], list[DoseLog]] = {}
    for log in logs:
        key = (log.item_id, log.scheduled_date)
        log_index.setdefault(key, []).append(log)

    total_expected = 0
    total_taken = 0
    total_skipped = 0

    item_stats: list[ItemAdherence] = []

    for item in items:
        item_expected = 0
        item_taken = 0
        item_skipped = 0

        current_date = start_date
        while current_date <= end_date:
            if _is_scheduled(item.schedule_days, current_date):
                item_expected += item.doses_per_day
                day_logs = log_index.get((item.id, current_date), [])
                item_taken += sum(1 for l in day_logs if l.status == "taken")
                item_skipped += sum(1 for l in day_logs if l.status == "skipped")
            current_date += datetime.timedelta(days=1)

        item_missed = max(0, item_expected - item_taken - item_skipped)
        pct = (item_taken / item_expected * 100) if item_expected > 0 else 0.0

        item_stats.append(
            ItemAdherence(
                item_id=item.id,
                item_name=item.name,
                expected=item_expected,
                taken=item_taken,
                skipped=item_skipped,
                missed=item_missed,
                adherence_pct=round(pct, 1),
            )
        )

        total_expected += item_expected
        total_taken += item_taken
        total_skipped += item_skipped

    overall_pct = (total_taken / total_expected * 100) if total_expected > 0 else 0.0

    # Compute streaks (days where ALL scheduled doses were taken)
    current_streak, longest_streak = _compute_streaks(items, log_index, end_date)

    return AdherenceStats(
        user_id=user_id,
        start_date=start_date,
        end_date=end_date,
        overall_adherence_pct=round(overall_pct, 1),
        items=item_stats,
        current_streak=current_streak,
        longest_streak=longest_streak,
    )


def _compute_streaks(
    items: list[Item],
    log_index: dict[tuple[int, datetime.date], list[DoseLog]],
    end_date: datetime.date,
) -> tuple[int, int]:
    """
    A 'perfect day' = every scheduled dose was taken (status='taken').
    Walks backwards from end_date to compute current and longest streaks.
    """
    current_streak = 0
    longest_streak = 0
    streak = 0
    still_current = True

    # Walk back up to 365 days
    for i in range(365):
        day = end_date - datetime.timedelta(days=i)
        day_perfect = True
        day_has_items = False

        for item in items:
            if _is_scheduled(item.schedule_days, day):
                day_has_items = True
                day_logs = log_index.get((item.id, day), [])
                taken_count = sum(1 for l in day_logs if l.status == "taken")
                if taken_count < item.doses_per_day:
                    day_perfect = False
                    break

        if not day_has_items:
            # No items scheduled this day — doesn't break streak, but doesn't extend it
            continue

        if day_perfect:
            streak += 1
            if still_current:
                current_streak = streak
            longest_streak = max(longest_streak, streak)
        else:
            still_current = False
            streak = 0

    return current_streak, longest_streak
