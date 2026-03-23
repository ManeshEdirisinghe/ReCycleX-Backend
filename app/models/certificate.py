from datetime import datetime
from sqlalchemy import String, Integer, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import BaseModel

class Certificate(BaseModel):
    __tablename__ = "certificates"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True, nullable=False)
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"), index=True, nullable=False, unique=True)
    
    reference_number: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    date_issued: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
    details: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    user = relationship("User", foreign_keys=[user_id], backref="certificates")
    item = relationship("EWasteItem", backref="certificate")
