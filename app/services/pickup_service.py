from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.pickup import PickupRequest
from app.models.item import EWasteItem
from app.models.enums import PickupStatus, ItemStatus
from app.schemas.pickup import (
    PickupRequestCreate,
    PickupRequestAdminApprove,
    PickupRequestAdminAssign,
    PickupRequestAgentUpdate,
)

def get(db: Session, id: int) -> Optional[PickupRequest]:
    stmt = select(PickupRequest).where(PickupRequest.id == id)
    return db.execute(stmt).scalar_one_or_none()

def get_by_item(db: Session, item_id: int) -> Optional[PickupRequest]:
    stmt = select(PickupRequest).where(PickupRequest.item_id == item_id)
    return db.execute(stmt).scalar_one_or_none()

def get_multi_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[PickupRequest]:
    stmt = select(PickupRequest).where(PickupRequest.user_id == user_id).offset(skip).limit(limit)
    return list(db.execute(stmt).scalars().all())

def get_multi_by_agent(db: Session, agent_id: int, skip: int = 0, limit: int = 100) -> List[PickupRequest]:
    stmt = select(PickupRequest).where(PickupRequest.agent_id == agent_id).offset(skip).limit(limit)
    return list(db.execute(stmt).scalars().all())

def create_with_item(
    db: Session, obj_in: PickupRequestCreate, user_id: int, item: EWasteItem
) -> PickupRequest:
    # Set item status
    item.status = ItemStatus.PICKUP_REQUESTED
    db.add(item)
    
    db_obj = PickupRequest(
        item_id=obj_in.item_id,
        user_id=user_id,
        scheduled_date=obj_in.scheduled_date,
        pickup_address=obj_in.pickup_address,
        notes=obj_in.notes,
        status=PickupStatus.REQUESTED
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    db.refresh(item)
    return db_obj

def approve(db: Session, db_obj: PickupRequest, obj_in: PickupRequestAdminApprove) -> PickupRequest:
    db_obj.status = PickupStatus.APPROVED
    if obj_in.scheduled_date:
        db_obj.scheduled_date = obj_in.scheduled_date
    if obj_in.notes:
        db_obj.notes = obj_in.notes
        
    # Optional: Update linked item status
    if db_obj.item:
        db_obj.item.status = ItemStatus.READY_FOR_PICKUP
        db.add(db_obj.item)
        
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def assign_agent(db: Session, db_obj: PickupRequest, agent_id: int) -> PickupRequest:
    db_obj.agent_id = agent_id
    db_obj.status = PickupStatus.ASSIGNED
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def agent_update(db: Session, db_obj: PickupRequest, obj_in: PickupRequestAgentUpdate) -> PickupRequest:
    db_obj.status = obj_in.status
    if obj_in.notes is not None:
        db_obj.notes = obj_in.notes
        
    # Sync item status conditionally
    if db_obj.item:
        if obj_in.status == PickupStatus.PICKED_UP:
            db_obj.item.status = ItemStatus.PICKED_UP
        elif obj_in.status == PickupStatus.CANCELED:
            db_obj.item.status = ItemStatus.PENDING_REVIEW # Revert
    
    db.add(db_obj)
    if db_obj.item:
        db.add(db_obj.item)
        
    db.commit()
    db.refresh(db_obj)
    return db_obj
