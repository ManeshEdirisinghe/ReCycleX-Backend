from app.core.exceptions import NotFoundException, ForbiddenException, BadRequestException, UnauthorizedException
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User
from app.schemas.item import EWasteItemCreate, EWasteItemResponse, EWasteItemUpdate
from app.services import item_service, category_service

router = APIRouter()

@router.post("/", response_model=EWasteItemResponse)
def create_item(
    *,
    db: Session = Depends(deps.get_db),
    item_in: EWasteItemCreate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Create new item. Default status will be PENDING_REVIEW.
    """
    category = category_service.get(db, id=item_in.category_id)
    if not category:
        raise NotFoundException(message="Category not found")
        
    item = item_service.create_with_user(db=db, obj_in=item_in, user_id=current_user.id)
    return item

@router.get("/my-items", response_model=List[EWasteItemResponse])
def read_my_items(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve own items.
    """
    items = item_service.get_multi_by_user(
        db=db, user_id=current_user.id, skip=skip, limit=limit
    )
    return items

@router.get("/{item_id}", response_model=EWasteItemResponse)
def read_item(
    *,
    db: Session = Depends(deps.get_db),
    item_id: int,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Get item by ID.
    User can only read their own items. Admin can read all.
    """
    item = item_service.get(db=db, id=item_id)
    if not item:
        raise NotFoundException(message="Item not found")
    if item.user_id != current_user.id and current_user.role != "ADMIN":
        raise ForbiddenException(message="Not enough permissions")
    return item

@router.put("/{item_id}", response_model=EWasteItemResponse)
def update_item(
    *,
    db: Session = Depends(deps.get_db),
    item_id: int,
    item_in: EWasteItemUpdate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Update an item.
    User can update their own item. Normal users can't override admin statuses arbitrarily without specific endpoints.
    """
    item = item_service.get(db=db, id=item_id)
    if not item:
        raise NotFoundException(message="Item not found")
    if item.user_id != current_user.id and current_user.role != "ADMIN":
        raise ForbiddenException(message="Not enough permissions")
    
    # Restrict normal users from updating status
    if current_user.role != "ADMIN" and item_in.status is not None:
        item_in.status = None # Ignore status updates from regular users
        
    if item_in.category_id is not None:
        category = category_service.get(db, id=item_in.category_id)
        if not category:
            raise NotFoundException(message="Category not found")
            
    item = item_service.update(db=db, db_obj=item, obj_in=item_in)
    return item

@router.delete("/{item_id}", response_model=EWasteItemResponse)
def delete_item(
    *,
    db: Session = Depends(deps.get_db),
    item_id: int,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Delete an item. User can delete own item.
    """
    item = item_service.get(db=db, id=item_id)
    if not item:
        raise NotFoundException(message="Item not found")
    if item.user_id != current_user.id and current_user.role != "ADMIN":
        raise ForbiddenException(message="Not enough permissions")
        
    item = item_service.remove(db=db, id=item_id)
    return item
