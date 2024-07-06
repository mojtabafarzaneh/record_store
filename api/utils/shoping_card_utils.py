import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from data.models.card import Card
from schema.shopin_card_schema import CreateCard


async def create_card(db: AsyncSession, card: CreateCard, user_id : uuid.UUID, record_id: uuid.UUID ):
    db_card = Card(**card.dict(), record_id=record_id, user_id=user_id) # type: ignore
    db.add(db_card)
    await db.commit()
    await db.refresh(db_card)
    return db_card

async def get_card(db: AsyncSession, card_id: uuid.UUID):
    query = select(Card).where(Card.id == card_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def get_cards(db:AsyncSession, fetch: int = 10):
    query = select(Card).order_by(Card.id).fetch(fetch)
    result = await db.execute(query)
    return result.scalars().all()
