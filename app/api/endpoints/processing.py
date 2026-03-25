from app.core.exceptions import NotFoundException, ForbiddenException, BadRequestException, UnauthorizedException
from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User
from app.schemas.processing import ItemProcessingCreate, ItemProcessingUpdate, ItemProcessingResponse
from app.services import processing_service, center_service, item_service

router = APIRouter()

def get_current_center_user(current_user: User = Depends(deps.get_current_user)) -> User:
    if current_user.role not in ["RECYCLING_CENTER", "REPAIR_CENTER"]:
        raise ForbiddenException(message="Not enough privileges. Must be a processing center.")
    return current_user

@router.post("/", response_model=ItemProcessingResponse)
def create_processing_record(
    *,
    db: Session = Depends(deps.get_db),
    processing_in: ItemProcessingCreate,
    current_center_user: User = Depends(get_current_center_user),
) -> Any:
    """
    Start processing an assigned item. Only assigned centers can do this.
    """
    center = center_service.get_by_user_id(db=db, user_id=current_center_user.id)
    if not center:
        raise NotFoundException(message="Center not found for user")
        
    item = item_service.get(db=db, id=processing_in.item_id)
    if not item:
        raise NotFoundException(message="Item not found")
        
    if item.assigned_center_id != center.id:
        raise ForbiddenException(message="Item is not assigned to your center")
        
    existing_record = processing_service.get_by_item(db=db, item_id=item.id)
    if existing_record:
        raise BadRequestException(message="Item already has an active processing record")
        
    record = processing_service.create(db=db, obj_in=processing_in, center_id=center.id, item=item)
    return record

@router.put("/{processing_id}", response_model=ItemProcessingResponse)
def update_processing_record(
    *,
    db: Session = Depends(deps.get_db),
    processing_id: int,
    processing_in: ItemProcessingUpdate,
    current_center_user: User = Depends(get_current_center_user),
) -> Any:
    """
    Complete processing by submitting final status. Only assigned centers can do this.
    """
    center = center_service.get_by_user_id(db=db, user_id=current_center_user.id)
    if not center:
        raise NotFoundException(message="Center not found for user")
        
    record = processing_service.get(db=db, id=processing_id)
    if not record:
        raise NotFoundException(message="Processing record not found")
        
    if record.center_id != center.id:
        raise ForbiddenException(message="Record does not belong to your center")
        
    record = processing_service.complete_processing(db=db, db_obj=record, obj_in=processing_in)
    return record

@router.get("/item/{item_id}", response_model=ItemProcessingResponse)
def read_processing_record_for_item(
    *,
    db: Session = Depends(deps.get_db),
    item_id: int,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Get processing record for a specific item. Admin, owner, and assigned center.
    """
    item = item_service.get(db=db, id=item_id)
    if not item:
        raise NotFoundException(message="Item not found")
        
    record = processing_service.get_by_item(db=db, item_id=item.id)
    if not record:
        raise NotFoundException(message="Processing record not found")
        
    # Check privileges
    if current_user.role != "ADMIN" and item.user_id != current_user.id:
        # Check if they are the center user
        center_user = None
        if current_user.role in ["RECYCLING_CENTER", "REPAIR_CENTER"]:
            center = center_service.get_by_user_id(db=db, user_id=current_user.id)
            if center and record.center_id == center.id:
                center_user = center
                
        if not center_user:
            raise ForbiddenException(message="Not enough privileges.")
            
    return record
