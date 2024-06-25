import enum
import uuid
from turtle import back

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from data.db_engine import Base


class AlbumGenre(enum.Enum):
    ROCK = "rock"
    POP = "pop"
    ELECTRONIC = "electronic"
    COUNTRY = "country"
    METAL = "metal"

class RecordType(enum.Enum):
    VYNIL = "vynil"
    CD = "cd"
    TAPE = "tape"

class Album(Base):
    __tablename__ = "album"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default_factory=uuid.uuid4)
    title : Mapped[str] = mapped_column(String(100) ,nullable=False, default=None)
    genre : Mapped[AlbumGenre] = mapped_column(SQLEnum(AlbumGenre), nullable=False, default=None)
    artist : Mapped[str] = mapped_column(String(100), nullable=False,default=None)
    tracks = relationship("tracks", back_populates="album") # type: ignore
    records = relationship("records", back_populates="album") # type: ignore



class Tracks(Base):
    __tablename__ = "tracks"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default_factory=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(100), nullable= False, default=None)
    album_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("album.id"), default=None)


class Records(Base):
    __tablename__ = "records"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default_factory=uuid.uuid4)

    record_type : Mapped[RecordType] = mapped_column(SQLEnum(RecordType), nullable=False, default=None)
    album_id : Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("album.id"), default=None)