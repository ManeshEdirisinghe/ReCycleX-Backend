from datetime import datetime
from sqlalchemy import String, Integer, Text, ForeignKey, DateTime, Enum as SQLEnum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import BaseModel
from app.models.enums import PickupStatus

class PickupRequest(BaseModel):
    __tablename__ = "pickup_requests"

    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"), index=True, nullable=False, unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True, nullable=False)
    agent_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), index=True, nullable=True)
    
    status: Mapped[PickupStatus] = mapped_column(SQLEnum(PickupStatus), default=PickupStatus.REQUESTED, nullable=False)
    
    requested_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
    scheduled_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    
    pickup_address: Mapped[str] = mapped_column(String(255), nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    item = relationship("EWasteItem", backref="pickup_request")
    user = relationship("User", foreign_keys=[user_id], backref="requested_pickups")
    agent = relationship("User", foreign_keys=[agent_id], backref="assigned_pickups")
