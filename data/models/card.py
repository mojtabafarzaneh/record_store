import uuid
from datetime import datetime

from sqlalchemy import DECIMAL, Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from data.db_engine import Base


class Card(Base):
    __tablename__ = "card"

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("user.id"))
    record_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("records.id"))
    quantity : Mapped[int] = mapped_column(Integer, nullable=False)
    price : Mapped[float] = mapped_column(DECIMAL(10,2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active : Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    """
    relationships
    """
    user: Mapped["User"] = relationship("User", back_populates="card") # type: ignore
    records : Mapped["Records"] = relationship("Records", back_populates="card") # type: ignore


    @property
    def total_price(self) -> float:
        return self.quantity * float(self.price)
