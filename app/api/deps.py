from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import ForbiddenException, NotFoundException, BadRequestException, UnauthorizedException
from app.db.session import SessionLocal
from app.models.user import User
from app.models.enums import Role
from app.schemas.token import TokenPayload
from app.services import user_service

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise UnauthorizedException(message="Could not validate credentials")
    
    if token_data.sub is None:
        raise UnauthorizedException(message="Invalid token payload")
    
    user = user_service.get_by_id(db, user_id=int(token_data.sub))
    if not user:
        raise NotFoundException(message="User not found")
    if not user.is_active:
        raise BadRequestException(message="Inactive user account")
    return user

def get_current_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.role != Role.ADMIN:
        raise ForbiddenException(message="Admin privileges required")
    return current_user
