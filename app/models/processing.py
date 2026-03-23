from datetime import datetime
from sqlalchemy import Integer, Text, ForeignKey, DateTime, Enum as SQLEnum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import BaseModel
from app.models.enums import ProcessType, FinalStatus

class ItemProcessing(BaseModel):
    __tablename__ = "item_processing"

    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"), index=True, nullable=False, unique=True)
    center_id: Mapped[int] = mapped_column(ForeignKey("processing_centers.id"), index=True, nullable=False)
    
    process_type: Mapped[ProcessType] = mapped_column(SQLEnum(ProcessType), nullable=False)
    final_status: Mapped[FinalStatus | None] = mapped_column(SQLEnum(FinalStatus), nullable=True) # Null until completed
    
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    process_date: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)

    # Relationships
    item = relationship("EWasteItem", backref="processing_record")
    center = relationship("ProcessingCenter", backref="processing_records")
