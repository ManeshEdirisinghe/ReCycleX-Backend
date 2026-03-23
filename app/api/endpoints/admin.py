from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User
from app.schemas.item import EWasteItemResponse
from app.schemas.category import CategoryCreate, CategoryResponse
from app.services import item_service, category_service

router = APIRouter()

@router.get("/items", response_model=List[EWasteItemResponse])
def read_all_items(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_admin: User = Depends(deps.get_current_admin),
) -> Any:
    """
    Retrieve all items. Admin only.
    """
    items = item_service.get_multi(db, skip=skip, limit=limit)
    return items

@router.post("/categories", response_model=CategoryResponse)
def create_category(
    *,
    db: Session = Depends(deps.get_db),
    category_in: CategoryCreate,
    current_admin: User = Depends(deps.get_current_admin),
) -> Any:
    """
    Create new category. Admin only.
    """
    category = category_service.get_by_name(db, name=category_in.name)
    if category:
        raise HTTPException(
            status_code=400,
            detail="A category with this name already exists.",
        )
    category = category_service.create(db, obj_in=category_in)
    return category
