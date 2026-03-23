from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class RewardBase(BaseModel):
    user_id: int
    item_id: int
    points_awarded: int

class RewardCreate(RewardBase):
    pass

class RewardInDBBase(RewardBase):
    id: int
    awarded_at: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class RewardResponse(RewardInDBBase):
    pass
