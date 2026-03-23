from typing import Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User
from app.schemas.certificate import CertificateResponse
from app.services import certificate_service

router = APIRouter()

@router.get("/my-certificates", response_model=List[CertificateResponse])
def read_my_certificates(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve own certificates.
    """
    certificates = certificate_service.get_multi_by_user(db=db, user_id=current_user.id, skip=skip, limit=limit)
    return certificates
