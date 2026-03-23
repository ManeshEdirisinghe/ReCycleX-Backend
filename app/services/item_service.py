from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.item import EWasteItem
from app.models.enums import ItemStatus
from app.schemas.item import EWasteItemCreate, EWasteItemUpdate

def get(db: Session, id: int) -> Optional[EWasteItem]:
    stmt = select(EWasteItem).where(EWasteItem.id == id)
    return db.execute(stmt).scalar_one_or_none()

def get_multi(db: Session, skip: int = 0, limit: int = 100) -> List[EWasteItem]:
    stmt = select(EWasteItem).offset(skip).limit(limit)
    return list(db.execute(stmt).scalars().all())

def get_multi_by_user(
    db: Session, user_id: int, skip: int = 0, limit: int = 100
) -> List[EWasteItem]:
    stmt = select(EWasteItem).where(EWasteItem.user_id == user_id).offset(skip).limit(limit)
    return list(db.execute(stmt).scalars().all())

def create_with_user(
    db: Session, obj_in: EWasteItemCreate, user_id: int
) -> EWasteItem:
    db_obj = EWasteItem(
        **obj_in.model_dump(),
        user_id=user_id,
        status=ItemStatus.PENDING_REVIEW
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update(
    db: Session, db_obj: EWasteItem, obj_in: EWasteItemUpdate
) -> EWasteItem:
    update_data = obj_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def remove(db: Session, id: int) -> EWasteItem:
    obj = get(db, id)
    db.delete(obj)
    db.commit()
    return obj
