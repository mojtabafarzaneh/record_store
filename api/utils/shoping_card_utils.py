import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from data.models.card import Card
from schema.shopin_card_schema import CreateCard


async def create_card(db: AsyncSession, card: CreateCard):
    db_card = Card(user_id= card.user_id, record_id=card.record_id, quantity = card.quantity, price = card.price, is_active = card.is_active) # type: ignore
    db.add(db_card)
    await db.commit()
    await db.refresh(db_card)
    return db_card