from typing import Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api import deps
from app.schemas.category import CategoryResponse
from app.services import category_service

router = APIRouter()

@router.get("/", response_model=List[CategoryResponse])
def read_categories(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve all available categories. Publicly accessible.
    """
    categories = category_service.get_multi(db, skip=skip, limit=limit)
    return categories
