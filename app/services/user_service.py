from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.enums import Role
from app.schemas.user import UserCreate, UserUpdate, UserRegister
from app.core.security import get_password_hash, verify_password


def get_by_email(db: Session, email: str) -> Optional[User]:
    stmt = select(User).where(User.email == email)
    result = db.execute(stmt)
    return result.scalar_one_or_none()

def get_by_id(db: Session, user_id: int) -> Optional[User]:
    stmt = select(User).where(User.id == user_id)
    result = db.execute(stmt)
    return result.scalar_one_or_none()

def authenticate(db: Session, email: str, password: str) -> Optional[User]:
    user = get_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def create(db: Session, obj_in: UserCreate) -> User:
    db_obj = User(
        email=obj_in.email,
        hashed_password=get_password_hash(obj_in.password),
        full_name=obj_in.full_name,
        phone_number=obj_in.phone_number,
        address=obj_in.address,
        role=obj_in.role,
        is_active=obj_in.is_active
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def register(db: Session, obj_in: UserRegister) -> User:
    db_obj = User(
        email=obj_in.email,
        hashed_password=get_password_hash(obj_in.password),
        full_name=obj_in.full_name,
        phone_number=obj_in.phone_number,
        address=obj_in.address,
        role=Role.USER,
        is_active=True,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update(db: Session, db_obj: User, obj_in: UserUpdate) -> User:
    update_data = obj_in.model_dump(exclude_unset=True)
    if "password" in update_data:
        hashed_password = get_password_hash(update_data["password"])
        del update_data["password"]
        update_data["hashed_password"] = hashed_password
        
    for field, value in update_data.items():
        setattr(db_obj, field, value)
        
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_multi(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    stmt = select(User).offset(skip).limit(limit)
    result = db.execute(stmt)
    return list(result.scalars().all())
