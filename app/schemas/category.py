from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    base_reward_points: int = 0

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    base_reward_points: Optional[int] = None

class CategoryInDBBase(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CategoryResponse(CategoryInDBBase):
    pass
