from typing import Dict
from pydantic import BaseModel
from app.models.enums import ItemStatus, PickupStatus

class DashboardSummaryResponse(BaseModel):
    total_users: int
    total_items: int
    total_pickups: int
    total_completed_items: int
    
    total_recycled_items: int
    total_repaired_items: int
    total_donated_items: int
    
    item_counts_by_status: Dict[ItemStatus, int]
    pickup_counts_by_status: Dict[PickupStatus, int]
