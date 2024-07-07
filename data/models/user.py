
import uuid

import bcrypt
from sqlalchemy import Integer, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from data.db_engine import Base
from data.models.card import Card


class User(Base):
    __tablename__ = "user"
    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    first_name: Mapped[str] = mapped_column(String, nullable=False, default=None)
    last_name: Mapped[str] = mapped_column(String, nullable=False, default= None)
    email: Mapped[str] = mapped_column(unique=True, nullable=False, index=True, default=None)
    password : Mapped[str] = mapped_column(String, nullable=False, default=None)

    card: Mapped[list[Card]] = relationship("Card", back_populates="user")
