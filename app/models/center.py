from sqlalchemy import String, Integer, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import BaseModel
from app.models.enums import CenterType

class ProcessingCenter(BaseModel):
    __tablename__ = "processing_centers"

    # User ID linking to the manager account for this center
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True, index=True, nullable=False)
    
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    center_type: Mapped[CenterType] = mapped_column(SQLEnum(CenterType), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    contact_number: Mapped[str | None] = mapped_column(String(20), nullable=True)

    # Relationships
    user = relationship("User", foreign_keys=[user_id], backref="processing_center")
