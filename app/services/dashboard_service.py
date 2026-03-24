from typing import Dict
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.item import EWasteItem
from app.models.pickup import PickupRequest
from app.models.processing import ItemProcessing
from app.models.enums import ItemStatus, PickupStatus, FinalStatus
from app.schemas.dashboard import DashboardSummaryResponse

def get_dashboard_summary(db: Session) -> DashboardSummaryResponse:
    # Basic counts
    total_users = db.execute(select(func.count(User.id))).scalar() or 0
    total_items = db.execute(select(func.count(EWasteItem.id))).scalar() or 0
    total_pickups = db.execute(select(func.count(PickupRequest.id))).scalar() or 0
    
    total_completed_items = db.execute(
        select(func.count(EWasteItem.id)).where(EWasteItem.status == ItemStatus.COMPLETED)
    ).scalar() or 0

    # Processing counts
    total_recycled = db.execute(
        select(func.count(ItemProcessing.id)).where(ItemProcessing.final_status == FinalStatus.RECYCLED)
    ).scalar() or 0
    
    total_repaired = db.execute(
        select(func.count(ItemProcessing.id)).where(ItemProcessing.final_status == FinalStatus.REPAIRED)
    ).scalar() or 0
    
    total_donated = db.execute(
        select(func.count(ItemProcessing.id)).where(ItemProcessing.final_status == FinalStatus.DONATED)
    ).scalar() or 0

    # Item counts by status
    item_status_counts = db.execute(
        select(EWasteItem.status, func.count(EWasteItem.id)).group_by(EWasteItem.status)
    ).all()
    item_counts_by_status_dict = {status: count for status, count in item_status_counts}
    # Ensure all enum values exist
    for status in ItemStatus:
        if status not in item_counts_by_status_dict:
            item_counts_by_status_dict[status] = 0

    # Pickup counts by status
    pickup_status_counts = db.execute(
        select(PickupRequest.status, func.count(PickupRequest.id)).group_by(PickupRequest.status)
    ).all()
    pickup_counts_by_status_dict = {status: count for status, count in pickup_status_counts}
    # Ensure all enum values exist
    for status in PickupStatus:
        if status not in pickup_counts_by_status_dict:
            pickup_counts_by_status_dict[status] = 0

    return DashboardSummaryResponse(
        total_users=total_users,
        total_items=total_items,
        total_pickups=total_pickups,
        total_completed_items=total_completed_items,
        total_recycled_items=total_recycled,
        total_repaired_items=total_repaired,
        total_donated_items=total_donated,
        item_counts_by_status=item_counts_by_status_dict,
        pickup_counts_by_status=pickup_counts_by_status_dict
    )
