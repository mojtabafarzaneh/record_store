import uuid
from datetime import datetime
from xmlrpc.client import boolean

from pydantic import BaseModel
from sqlalchemy import true


class BaseCard(BaseModel):
    quantity : int
    price: float
    is_active : bool

class CreateCard(BaseCard):
    ...


class Card(BaseCard):
    id: uuid.UUID
    total_price : float
    user_id : uuid.UUID
    record_id : uuid.UUID

    class Config:
        from_attributes = True