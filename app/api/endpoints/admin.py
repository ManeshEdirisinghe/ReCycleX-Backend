from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User
from app.schemas.category import CategoryCreate, CategoryResponse
from app.schemas.center import ProcessingCenterCreate, ProcessingCenterResponse
from app.schemas.dashboard import DashboardSummaryResponse
from app.schemas.item import EWasteItemResponse
from app.schemas.pickup import (
    PickupRequestAdminApprove,
    PickupRequestAdminAssign,
    PickupRequestResponse,
)
from app.core.exceptions import BadRequestException, NotFoundException
from app.services import (
    category_service,
    center_service,
    dashboard_service,
    item_service,
    pickup_service,
    processing_service,
    user_service,
)

router = APIRouter()


# ---------------------------------------------------------------------------
# Items
# ---------------------------------------------------------------------------

@router.get("/items", response_model=List[EWasteItemResponse])
def read_all_items(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_admin: User = Depends(deps.get_current_admin),
) -> Any:
    """Retrieve all items. Admin only."""
    return item_service.get_multi(db, skip=skip, limit=limit)


# ---------------------------------------------------------------------------
# Categories
# ---------------------------------------------------------------------------

@router.post("/categories", response_model=CategoryResponse)
def create_category(
    *,
    db: Session = Depends(deps.get_db),
    category_in: CategoryCreate,
    current_admin: User = Depends(deps.get_current_admin),
) -> Any:
    """Create new category. Admin only."""
    if category_service.get_by_name(db, name=category_in.name):
        raise BadRequestException(message="A category with this name already exists.")
    return category_service.create(db, obj_in=category_in)


# ---------------------------------------------------------------------------
# Pickups
# ---------------------------------------------------------------------------

@router.put("/pickups/{pickup_id}/approve", response_model=PickupRequestResponse)
def approve_pickup(
    *,
    db: Session = Depends(deps.get_db),
    pickup_id: int,
    pickup_in: PickupRequestAdminApprove,
    current_admin: User = Depends(deps.get_current_admin),
) -> Any:
    """Approve a pickup request and optionally schedule a date."""
    pickup = pickup_service.get(db=db, id=pickup_id)
    if not pickup:
        raise NotFoundException(message="Pickup request not found.")
    return pickup_service.approve(db=db, db_obj=pickup, obj_in=pickup_in)


@router.put("/pickups/{pickup_id}/assign-agent", response_model=PickupRequestResponse)
def assign_pickup_agent(
    *,
    db: Session = Depends(deps.get_db),
    pickup_id: int,
    pickup_in: PickupRequestAdminAssign,
    current_admin: User = Depends(deps.get_current_admin),
) -> Any:
    """Assign a pickup to an agent."""
    pickup = pickup_service.get(db=db, id=pickup_id)
    if not pickup:
        raise NotFoundException(message="Pickup request not found.")
    agent = user_service.get_by_id(db=db, user_id=pickup_in.agent_id)
    if not agent or agent.role != "PICKUP_AGENT":
        raise BadRequestException(message="Valid PICKUP_AGENT not found.")
    return pickup_service.assign_agent(db=db, db_obj=pickup, agent_id=pickup_in.agent_id)


# ---------------------------------------------------------------------------
# Centers
# ---------------------------------------------------------------------------

@router.post("/centers", response_model=ProcessingCenterResponse)
def create_center(
    *,
    db: Session = Depends(deps.get_db),
    center_in: ProcessingCenterCreate,
    current_admin: User = Depends(deps.get_current_admin),
) -> Any:
    """Register a new Processing Center. Admin only."""
    user = user_service.get_by_id(db=db, user_id=center_in.user_id)
    if not user:
        raise NotFoundException(message="User not found.")
    if user.role not in ["RECYCLING_CENTER", "REPAIR_CENTER"]:
        raise BadRequestException(message="Provided user does not have a center role.")
    if center_service.get_by_user_id(db=db, user_id=center_in.user_id):
        raise BadRequestException(message="User already manages a processing center.")
    return center_service.create(db=db, obj_in=center_in)


@router.get("/centers", response_model=List[ProcessingCenterResponse])
def read_all_centers(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_admin: User = Depends(deps.get_current_admin),
) -> Any:
    """Retrieve all registered Processing Centers. Admin only."""
    return center_service.get_multi(db, skip=skip, limit=limit)


# ---------------------------------------------------------------------------
# Item → Center assignment
# ---------------------------------------------------------------------------

class ItemCenterAssign(BaseModel):
    center_id: int


@router.put("/items/{item_id}/assign-center", response_model=EWasteItemResponse)
def assign_center_to_item(
    *,
    db: Session = Depends(deps.get_db),
    item_id: int,
    item_in: ItemCenterAssign,
    current_admin: User = Depends(deps.get_current_admin),
) -> Any:
    """Assign a processing center to an item. Admin only."""
    item = item_service.get(db=db, id=item_id)
    if not item:
        raise NotFoundException(message="Item not found.")
    if not center_service.get(db=db, id=item_in.center_id):
        raise NotFoundException(message="Processing center not found.")
    return processing_service.assign_center(db=db, item=item, center_id=item_in.center_id)


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------

@router.get("/dashboard", response_model=DashboardSummaryResponse)
def read_dashboard_summary(
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_admin),
) -> Any:
    """Retrieve admin dashboard summary metrics. Admin only."""
    return dashboard_service.get_dashboard_summary(db=db)
