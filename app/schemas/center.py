from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from app.models.enums import CenterType

class ProcessingCenterBase(BaseModel):
    user_id: int
    name: str
    center_type: CenterType
    address: str
    contact_number: Optional[str] = None

class ProcessingCenterCreate(ProcessingCenterBase):
    pass

class ProcessingCenterUpdate(BaseModel):
    name: Optional[str] = None
    center_type: Optional[CenterType] = None
    address: Optional[str] = None
    contact_number: Optional[str] = None

class ProcessingCenterInDBBase(ProcessingCenterBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ProcessingCenterResponse(ProcessingCenterInDBBase):
    pass
