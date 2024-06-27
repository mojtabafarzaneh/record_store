import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from data.models.user import User
from schema.user_schema import CreateUser


async def get_user(db: AsyncSession, user_id: uuid.UUID):
    query = select(User).where(User.id == user_id)
    result = await db.execute(query) # type: ignore
    return result.scalar_one_or_none()