from typing import Any, List, Dict
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User
from app.schemas.reward import RewardResponse
from app.services import reward_service

router = APIRouter()

@router.get("/my-rewards", response_model=List[RewardResponse])
def read_my_rewards(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve own rewards.
    """
    rewards = reward_service.get_multi_by_user(db=db, user_id=current_user.id, skip=skip, limit=limit)
    return rewards

@router.get("/my-points", response_model=Dict[str, int])
def read_my_points(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve total reward points for the current user.
    """
    total_points = reward_service.get_total_points_by_user(db=db, user_id=current_user.id)
    return {"total_points": total_points}
