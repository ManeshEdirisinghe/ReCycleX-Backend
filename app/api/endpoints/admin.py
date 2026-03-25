from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User
from app.schemas.item import EWasteItemResponse
from app.schemas.category import CategoryCreate, CategoryResponse
from app.services import item_service, category_service

router = APIRouter()

@router.get("/items", response_model=List[EWasteItemResponse])
def read_all_items(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_admin: User = Depends(deps.get_current_admin),
) -> Any:
    """
    Retrieve all items. Admin only.
    """
    items = item_service.get_multi(db, skip=skip, limit=limit)
    return items

@router.post("/categories", response_model=CategoryResponse)
def create_category(
    *,
    db: Session = Depends(deps.get_db),
    category_in: CategoryCreate,
    current_admin: User = Depends(deps.get_current_admin),
) -> Any:
    """
    Create new category. Admin only.
    """
    category = category_service.get_by_name(db, name=category_in.name)
    if category:
        raise HTTPException(
            status_code=400,
            detail="A category with this name already exists.",
        )
    category = category_service.create(db, obj_in=category_in)
    return category

from app.schemas.pickup import PickupRequestResponse, PickupRequestAdminApprove, PickupRequestAdminAssign
from app.services import pickup_service, user_service

@router.put("/pickups/{pickup_id}/approve", response_model=PickupRequestResponse)
def approve_pickup(
    *,
    db: Session = Depends(deps.get_db),
    pickup_id: int,
    pickup_in: PickupRequestAdminApprove,
    current_admin: User = Depends(deps.get_current_admin),
) -> Any:
    """
    Approve a pickup request and optionally schedule a date.
    """
    pickup = pickup_service.get(db=db, id=pickup_id)
    if not pickup:
        raise HTTPException(status_code=404, detail="Pickup request not found.")
    
    pickup = pickup_service.approve(db=db, db_obj=pickup, obj_in=pickup_in)
    return pickup

@router.put("/pickups/{pickup_id}/assign-agent", response_model=PickupRequestResponse)
def assign_pickup_agent(
    *,
    db: Session = Depends(deps.get_db),
    pickup_id: int,
    pickup_in: PickupRequestAdminAssign,
    current_admin: User = Depends(deps.get_current_admin),
) -> Any:
    """
    Assign a pickup to an agent.
    """
    pickup = pickup_service.get(db=db, id=pickup_id)
    if not pickup:
        raise HTTPException(status_code=404, detail="Pickup request not found.")
        
    agent = user_service.get_by_id(db=db, user_id=pickup_in.agent_id)
    if not agent or agent.role != "PICKUP_AGENT":
        raise HTTPException(status_code=400, detail="Valid PICKUP_AGENT not found.")
        
    pickup = pickup_service.assign_agent(db=db, db_obj=pickup, agent_id=pickup_in.agent_id)
    return pickup

from app.schemas.center import ProcessingCenterCreate, ProcessingCenterResponse
from app.services import center_service

@router.post("/centers", response_model=ProcessingCenterResponse)
def create_center(
    *,
    db: Session = Depends(deps.get_db),
    center_in: ProcessingCenterCreate,
    current_admin: User = Depends(deps.get_current_admin),
) -> Any:
    """
    Register a new Processing Center. Admin only.
    """
    user = user_service.get_by_id(db=db, user_id=center_in.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    if user.role not in ["RECYCLING_CENTER", "REPAIR_CENTER"]:
        raise HTTPException(status_code=400, detail="Provided user does not have a center role.")
        
    existing_center = center_service.get_by_user_id(db=db, user_id=center_in.user_id)
    if existing_center:
        raise HTTPException(status_code=400, detail="User already manages a processing center.")
        
    center = center_service.create(db=db, obj_in=center_in)
    return center

@router.get("/centers", response_model=List[ProcessingCenterResponse])
def read_all_centers(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_admin: User = Depends(deps.get_current_admin),
) -> Any:
    """
    Retrieve all registered Processing Centers. Admin only.
    """
    centers = center_service.get_multi(db, skip=skip, limit=limit)
    return centers

from pydantic import BaseModel
from app.services import processing_service

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
    """
    Assign a processing center to an item explicitly. Admin only.
    """
    item = item_service.get(db=db, id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found.")
        
    center = center_service.get(db=db, id=item_in.center_id)
    if not center:
        raise HTTPException(status_code=404, detail="Processing center not found.")
        
    updated_item = processing_service.assign_center(db=db, item=item, center_id=item_in.center_id)
    return updated_item

from app.schemas.dashboard import DashboardSummaryResponse
from app.services import dashboard_service

@router.get("/dashboard", response_model=DashboardSummaryResponse)
def read_dashboard_summary(
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_admin),
) -> Any:
    """
    Retrieve admin dashboard summary metrics. Admin only.
    """
    summary = dashboard_service.get_dashboard_summary(db=db)
    return summary
