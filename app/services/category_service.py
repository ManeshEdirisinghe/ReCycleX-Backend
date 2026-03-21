from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate

def get(db: Session, id: int) -> Optional[Category]:
    stmt = select(Category).where(Category.id == id)
    return db.execute(stmt).scalar_one_or_none()

def get_by_name(db: Session, name: str) -> Optional[Category]:
    stmt = select(Category).where(Category.name == name)
    return db.execute(stmt).scalar_one_or_none()

def get_multi(db: Session, skip: int = 0, limit: int = 100) -> List[Category]:
    stmt = select(Category).offset(skip).limit(limit)
    return list(db.execute(stmt).scalars().all())

def create(db: Session, obj_in: CategoryCreate) -> Category:
    db_obj = Category(**obj_in.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update(db: Session, db_obj: Category, obj_in: CategoryUpdate) -> Category:
    update_data = obj_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def remove(db: Session, id: int) -> Category:
    obj = get(db, id)
    db.delete(obj)
    db.commit()
    return obj
