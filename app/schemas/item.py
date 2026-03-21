from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from app.models.enums import ItemCondition, ItemStatus

class EWasteItemBase(BaseModel):
    category_id: int
    title: str
    description: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    image_url: Optional[str] = None
    condition: ItemCondition

class EWasteItemCreate(EWasteItemBase):
    pass

class EWasteItemUpdate(BaseModel):
    category_id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    image_url: Optional[str] = None
    condition: Optional[ItemCondition] = None
    status: Optional[ItemStatus] = None # Admin can update status

class EWasteItemInDBBase(EWasteItemBase):
    id: int
    user_id: int
    status: ItemStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class EWasteItemResponse(EWasteItemInDBBase):
    pass
