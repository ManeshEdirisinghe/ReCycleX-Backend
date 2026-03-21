from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from app.models.enums import PickupStatus

class PickupRequestBase(BaseModel):
    item_id: int
    scheduled_date: Optional[datetime] = None
    pickup_address: str
    notes: Optional[str] = None

class PickupRequestCreate(PickupRequestBase):
    pass

class PickupRequestUpdate(BaseModel):
    scheduled_date: Optional[datetime] = None
    pickup_address: Optional[str] = None
    notes: Optional[str] = None

class PickupRequestAdminApprove(BaseModel):
    scheduled_date: Optional[datetime] = None
    notes: Optional[str] = None

class PickupRequestAdminAssign(BaseModel):
    agent_id: int

class PickupRequestAgentUpdate(BaseModel):
    status: PickupStatus
    notes: Optional[str] = None

class PickupRequestInDBBase(PickupRequestBase):
    id: int
    user_id: int
    agent_id: Optional[int] = None
    status: PickupStatus
    requested_at: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PickupRequestResponse(PickupRequestInDBBase):
    pass
