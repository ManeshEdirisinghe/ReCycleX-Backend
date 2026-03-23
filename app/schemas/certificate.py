from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class CertificateBase(BaseModel):
    user_id: int
    item_id: int
    reference_number: str
    details: Optional[str] = None

class CertificateCreate(CertificateBase):
    pass

class CertificateInDBBase(CertificateBase):
    id: int
    date_issued: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CertificateResponse(CertificateInDBBase):
    pass
