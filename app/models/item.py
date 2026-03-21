from sqlalchemy import String, Integer, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import BaseModel
from app.models.enums import ItemCondition, ItemStatus

class EWasteItem(BaseModel):
    __tablename__ = "items"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True, nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), index=True, nullable=False)
    
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    brand: Mapped[str | None] = mapped_column(String(100), nullable=True)
    model: Mapped[str | None] = mapped_column(String(100), nullable=True)
    image_url: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    
    condition: Mapped[ItemCondition] = mapped_column(SQLEnum(ItemCondition), nullable=False)
    status: Mapped[ItemStatus] = mapped_column(SQLEnum(ItemStatus), default=ItemStatus.PENDING_REVIEW, nullable=False)

    # Relationships (Optional but good for ORM)
    user = relationship("User", backref="items")
    category = relationship("Category", backref="items")
