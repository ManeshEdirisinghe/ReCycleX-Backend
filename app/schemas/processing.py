from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from app.models.enums import ProcessType, FinalStatus

class ItemProcessingBase(BaseModel):
    item_id: int
    process_type: ProcessType
    notes: Optional[str] = None

class ItemProcessingCreate(ItemProcessingBase):
    pass

class ItemProcessingUpdate(BaseModel):
    final_status: FinalStatus
    notes: Optional[str] = None

class ItemProcessingInDBBase(ItemProcessingBase):
    id: int
    center_id: int
    final_status: Optional[FinalStatus] = None
    process_date: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ItemProcessingResponse(ItemProcessingInDBBase):
    pass
