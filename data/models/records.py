import enum
import uuid
from os import name
from turtle import back

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from data.db_engine import Base
from data.models.card import Card


class AlbumGenre(enum.Enum):
    ROCK = "ROCK"
    POP = "POP"
    ELECTRONIC = "ELECTRONIC"
    COUNTRY = "COUNTRY"
    METAL = "METAL"

class RecordType(enum.Enum):
    VYNIL = "vynil"
    CD = "cd"
    TAPE = "tape"

class Album(Base):
    __tablename__ = "album"
    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title : Mapped[str] = mapped_column(String(100) ,nullable=False, default=None)
    genre : Mapped[AlbumGenre] = mapped_column(SQLEnum(AlbumGenre, name="albumgenre"), nullable=False)
    artist : Mapped[str] = mapped_column(String(100), nullable=False,default=None)

    tracks : Mapped["Tracks"] = relationship("Tracks")
    records : Mapped["Records"] = relationship("Records", back_populates="album")




class Tracks(Base):
    __tablename__ = "tracks"
    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(100), nullable= False, default=None)
    album_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("album.id"))

    album: Mapped[Album] = relationship("Album", back_populates="tracks")


class Records(Base):
    __tablename__ = "records"
    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    record_type : Mapped[RecordType] = mapped_column(SQLEnum(RecordType), nullable=False)
    album_id : Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("album.id"))

    card : Mapped[Card] = relationship("Card", back_populates="records")
    album : Mapped[Album] = relationship("Album", back_populates="records")