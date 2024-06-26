
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
    _password_hash : Mapped[str] = mapped_column('password', String, nullable=False, default=None)

    card: Mapped[list[Card]] = relationship("Card", back_populates="user")

    @hybrid_property
    def password(self) -> str: # type: ignore
        raise AttributeError("passwords are write only")

    @password.setter # type: ignore
    def password(self, plaintext_password: str) -> None:
        self._password_hash = bcrypt.hashpw(plaintext_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, plaintext_password: str) -> bool:
        return bcrypt.checkpw(plaintext_password.encode('utf-8'), self._password_hash.encode('utf-8'))
