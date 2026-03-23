from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.center import ProcessingCenter
from app.models.item import EWasteItem
from app.schemas.center import ProcessingCenterCreate, ProcessingCenterUpdate

def get(db: Session, id: int) -> Optional[ProcessingCenter]:
    stmt = select(ProcessingCenter).where(ProcessingCenter.id == id)
    return db.execute(stmt).scalar_one_or_none()

def get_by_user_id(db: Session, user_id: int) -> Optional[ProcessingCenter]:
    stmt = select(ProcessingCenter).where(ProcessingCenter.user_id == user_id)
    return db.execute(stmt).scalar_one_or_none()

def get_multi(db: Session, skip: int = 0, limit: int = 100) -> List[ProcessingCenter]:
    stmt = select(ProcessingCenter).offset(skip).limit(limit)
    return list(db.execute(stmt).scalars().all())

def create(db: Session, obj_in: ProcessingCenterCreate) -> ProcessingCenter:
    db_obj = ProcessingCenter(**obj_in.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update(db: Session, db_obj: ProcessingCenter, obj_in: ProcessingCenterUpdate) -> ProcessingCenter:
    update_data = obj_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_assigned_items(db: Session, center_id: int, skip: int = 0, limit: int = 100) -> List[EWasteItem]:
    stmt = select(EWasteItem).where(EWasteItem.assigned_center_id == center_id).offset(skip).limit(limit)
    return list(db.execute(stmt).scalars().all())
