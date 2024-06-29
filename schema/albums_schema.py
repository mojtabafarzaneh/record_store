import uuid

from pydantic import BaseModel


class BaseAlbum(BaseModel):
    title: str
    genre : str
    artist : str

class CreateAlbum(BaseAlbum):
    ...

class Album(BaseAlbum):
    id : uuid.UUID
    track_id : uuid.UUID

    class Config:
        from_attributes = True