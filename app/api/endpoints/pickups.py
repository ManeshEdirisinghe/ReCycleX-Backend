from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User
from app.schemas.pickup import PickupRequestCreate, PickupRequestResponse
from app.services import pickup_service, item_service

router = APIRouter()

@router.post("/", response_model=PickupRequestResponse)
def create_pickup(
    *,
    db: Session = Depends(deps.get_db),
    pickup_in: PickupRequestCreate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Create a new pickup request for an owned item.
    """
    item = item_service.get(db=db, id=pickup_in.item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if item.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions. You do not own this item.")
    
    # Check if there's already an active pickup request
    existing = pickup_service.get_by_item(db=db, item_id=pickup_in.item_id)
    if existing:
        raise HTTPException(status_code=400, detail="Pickup already requested for this item.")
        
    pickup = pickup_service.create_with_item(db=db, obj_in=pickup_in, user_id=current_user.id, item=item)
    return pickup

@router.get("/my-pickups", response_model=List[PickupRequestResponse])
def read_my_pickups(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve own pickups.
    """
    pickups = pickup_service.get_multi_by_user(db=db, user_id=current_user.id, skip=skip, limit=limit)
    return pickups

@router.get("/{pickup_id}", response_model=PickupRequestResponse)
def read_pickup(
    *,
    db: Session = Depends(deps.get_db),
    pickup_id: int,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Get pickup by ID. Owner or admin/agent only.
    """
    pickup = pickup_service.get(db=db, id=pickup_id)
    if not pickup:
        raise HTTPException(status_code=404, detail="Pickup request not found")
        
    if pickup.user_id != current_user.id and current_user.role not in ["ADMIN", "PICKUP_AGENT"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # If agent, verify they are assigned
    if current_user.role == "PICKUP_AGENT" and pickup.agent_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not assigned to this pickup")
        
    return pickup
