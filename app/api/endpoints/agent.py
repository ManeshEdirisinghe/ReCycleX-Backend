from app.core.exceptions import NotFoundException, ForbiddenException, BadRequestException, UnauthorizedException
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User
from app.schemas.pickup import PickupRequestResponse, PickupRequestAgentUpdate
from app.services import pickup_service

router = APIRouter()

def get_current_agent(current_user: User = Depends(deps.get_current_user)) -> User:
    if current_user.role != "PICKUP_AGENT":
        raise ForbiddenException(message="Not enough privileges. Must be PICKUP_AGENT")
    return current_user

@router.get("/pickups", response_model=List[PickupRequestResponse])
def read_agent_pickups(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_agent: User = Depends(get_current_agent),
) -> Any:
    """
    Retrieve pickups assigned to the current agent.
    """
    pickups = pickup_service.get_multi_by_agent(db=db, agent_id=current_agent.id, skip=skip, limit=limit)
    return pickups

@router.put("/pickups/{pickup_id}/status", response_model=PickupRequestResponse)
def update_pickup_status(
    *,
    db: Session = Depends(deps.get_db),
    pickup_id: int,
    pickup_in: PickupRequestAgentUpdate,
    current_agent: User = Depends(get_current_agent),
) -> Any:
    """
    Update status of an assigned pickup as an agent.
    """
    pickup = pickup_service.get(db=db, id=pickup_id)
    if not pickup:
        raise NotFoundException(message="Pickup request not found.")
        
    if pickup.agent_id != current_agent.id:
        raise ForbiddenException(message="You are not assigned to this pickup.")
        
    pickup = pickup_service.agent_update(db=db, db_obj=pickup, obj_in=pickup_in)
    return pickup
