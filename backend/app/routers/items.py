from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.item import Item
from app.models.user import User
from app.schemas.item import ItemCreate, ItemUpdate, ItemOut

router = APIRouter(prefix="/items", tags=["items"])


# ---- helpers ----

def _get_item_or_404(item_id: int, db: Session) -> Item:
    item = db.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


def _verify_user_exists(user_id: int, db: Session) -> None:
    if not db.get(User, user_id):
        raise HTTPException(status_code=404, detail="User not found")


# ---- endpoints ----

@router.post("/", response_model=ItemOut, status_code=status.HTTP_201_CREATED)
def create_item(payload: ItemCreate, db: Session = Depends(get_db)):
    _verify_user_exists(payload.user_id, db)
    item = Item(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


# IMPORTANT: /by-user/ declared ABOVE /{item_id} to avoid route shadowing
@router.get("/by-user/{user_id}", response_model=list[ItemOut])
def list_items_for_user(
    user_id: int,
    active_only: bool = False,
    db: Session = Depends(get_db),
):
    _verify_user_exists(user_id, db)
    query = db.query(Item).filter(Item.user_id == user_id)
    if active_only:
        query = query.filter(Item.active == True)  # noqa: E712
    return query.all()


@router.get("/{item_id}", response_model=ItemOut)
def get_item(item_id: int, db: Session = Depends(get_db)):
    return _get_item_or_404(item_id, db)


@router.patch("/{item_id}", response_model=ItemOut)
def update_item(item_id: int, payload: ItemUpdate, db: Session = Depends(get_db)):
    item = _get_item_or_404(item_id, db)
    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(item, k, v)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = _get_item_or_404(item_id, db)
    db.delete(item)
    db.commit()
    return
