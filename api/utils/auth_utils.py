import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.utils.secrets import pwd_context
from data.models.user import User
from schema.user_schema import CreateUser


async def auth_user(db: AsyncSession, user_email: str) :
    query = select(User).where(User.email == user_email)
    q_user = await db.execute(query)

    return q_user.scalar_one_or_none()
