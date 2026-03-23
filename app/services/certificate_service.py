import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.certificate import Certificate
from app.schemas.certificate import CertificateCreate

def get_multi_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Certificate]:
    stmt = select(Certificate).where(Certificate.user_id == user_id).offset(skip).limit(limit)
    return list(db.execute(stmt).scalars().all())

def generate_certificate(db: Session, user_id: int, item_id: int, details: Optional[str] = None) -> Certificate:
    # generate a somewhat formal looking reference string
    ref = f"CERT-{datetime.utcnow().strftime('%Y%m%d')}-{str(uuid.uuid4()).split('-')[0].upper()}"
    
    db_obj = Certificate(
        user_id=user_id,
        item_id=item_id,
        reference_number=ref,
        details=details
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
