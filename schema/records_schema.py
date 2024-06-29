import uuid

from pydantic import BaseModel


class BaseRecords(BaseModel):
    record_type : str
    album_id : uuid.UUID


class CreateRecords(BaseRecords):
    ...

class Records(BaseRecords):
    id : uuid.UUID

    class Config:
        from_attributes =  True
