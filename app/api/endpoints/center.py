from app.core.exceptions import NotFoundException, ForbiddenException, BadRequestException, UnauthorizedException
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User
from app.schemas.center import ProcessingCenterResponse
from app.schemas.item import EWasteItemResponse

from app.services import center_service

router = APIRouter()

def get_current_center_user(current_user: User = Depends(deps.get_current_user)) -> User:
    if current_user.role not in ["RECYCLING_CENTER", "REPAIR_CENTER"]:
        raise ForbiddenException(message="Not enough privileges. Must be a processing center.")
    return current_user

@router.get("/profile", response_model=ProcessingCenterResponse)
def read_center_profile(
    db: Session = Depends(deps.get_db),
    current_center_user: User = Depends(get_current_center_user),
) -> Any:
    """
    Get the Processing Center profile assigned to the current user manager.
    """
    center = center_service.get_by_user_id(db=db, user_id=current_center_user.id)
    if not center:
        raise NotFoundException(message="Processing center has not been registered to this account by the Admin.")
    return center

@router.get("/items", response_model=List[EWasteItemResponse])
def read_assigned_items(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_center_user: User = Depends(get_current_center_user),
) -> Any:
    """
    Retrieve items assigned to the current center.
    """
    center = center_service.get_by_user_id(db=db, user_id=current_center_user.id)
    if not center:
        raise NotFoundException(message="Processing center has not been registered to this account.")
        
    items = center_service.get_assigned_items(db=db, center_id=center.id, skip=skip, limit=limit)
    return items
