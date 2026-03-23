from typing import List
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.reward import Reward
from app.schemas.reward import RewardCreate

def get_multi_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Reward]:
    stmt = select(Reward).where(Reward.user_id == user_id).offset(skip).limit(limit)
    return list(db.execute(stmt).scalars().all())

def get_total_points_by_user(db: Session, user_id: int) -> int:
    stmt = select(func.sum(Reward.points_awarded)).where(Reward.user_id == user_id)
    result = db.execute(stmt).scalar()
    return result or 0

def create(db: Session, obj_in: RewardCreate) -> Reward:
    db_obj = Reward(
        user_id=obj_in.user_id,
        item_id=obj_in.item_id,
        points_awarded=obj_in.points_awarded
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
