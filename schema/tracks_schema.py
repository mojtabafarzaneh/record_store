import uuid

from pydantic import BaseModel


class BaseTrack(BaseModel):
    title : str
    album_id : uuid.UUID

class CreateTrack(BaseTrack):
    ...

class Track(BaseTrack):
    id : uuid.UUID

    class Config:
        from_attributes = True