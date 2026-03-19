from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.enums import Role
from app.schemas.user import UserCreate
from app.services import user_service

def init_db(db: Session) -> None:
    user = user_service.get_by_email(db, email=settings.FIRST_SUPERUSER_EMAIL)
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER_EMAIL,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            full_name="Super Admin",
            role=Role.ADMIN,
            is_active=True,
        )
        user = user_service.create(db, obj_in=user_in)
