from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.processing import ItemProcessing
from app.models.item import EWasteItem
from app.models.center import ProcessingCenter
from app.models.enums import ItemStatus
from app.schemas.processing import ItemProcessingCreate, ItemProcessingUpdate

def get(db: Session, id: int) -> Optional[ItemProcessing]:
    stmt = select(ItemProcessing).where(ItemProcessing.id == id)
    return db.execute(stmt).scalar_one_or_none()

def get_by_item(db: Session, item_id: int) -> Optional[ItemProcessing]:
    stmt = select(ItemProcessing).where(ItemProcessing.item_id == item_id)
    return db.execute(stmt).scalar_one_or_none()

def assign_center(db: Session, item: EWasteItem, center_id: int) -> EWasteItem:
    item.assigned_center_id = center_id
    item.status = ItemStatus.ASSIGNED_TO_CENTER
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def create(
    db: Session, obj_in: ItemProcessingCreate, center_id: int, item: EWasteItem
) -> ItemProcessing:
    item.status = ItemStatus.IN_PROCESSING
    db.add(item)
    
    db_obj = ItemProcessing(
        item_id=obj_in.item_id,
        center_id=center_id,
        process_type=obj_in.process_type,
        notes=obj_in.notes
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    db.refresh(item)
    return db_obj

def complete_processing(db: Session, db_obj: ItemProcessing, obj_in: ItemProcessingUpdate) -> ItemProcessing:
    from app.services import reward_service, certificate_service
    from app.schemas.reward import RewardCreate
    from app.models.enums import FinalStatus

    db_obj.final_status = obj_in.final_status
    if obj_in.notes is not None:
        db_obj.notes = obj_in.notes
        
    if db_obj.item:
        db_obj.item.status = ItemStatus.COMPLETED
        db.add(db_obj.item)
        
        # Trigger Reward & Certificate logic
        if obj_in.final_status in [FinalStatus.RECYCLED, FinalStatus.REPAIRED, FinalStatus.DONATED]:
            # Give points based on item category
            points = 0
            if db_obj.item.category:
                points = db_obj.item.category.base_reward_points
                
            # Create Reward
            if points > 0:
                reward_in = RewardCreate(
                    user_id=db_obj.item.user_id,
                    item_id=db_obj.item.id,
                    points_awarded=points
                )
                reward_service.create(db=db, obj_in=reward_in)
                
            # Create Certificate
            certificate_service.generate_certificate(
                db=db, 
                user_id=db_obj.item.user_id, 
                item_id=db_obj.item.id,
                details=f"Item {obj_in.final_status.value} processed successfully."
            )
        
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
