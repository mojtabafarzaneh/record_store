import uuid
from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import true


class BaseCard(BaseModel):
    price: int
    created_at : datetime
    updated_at : datetime
    is_active : bool

class Create_card(BaseCard):
    user_id : uuid.UUID
    records_id : uuid.UUID
    quantity : int


class Card(BaseCard):
    id: uuid.UUID
    total_price : float

    class Config:
        from_attributes = true