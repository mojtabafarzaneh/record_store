import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.utils.secrets import pwd_context
from data.models.user import User
from schema.user_schema import AuthUser, CreateUser


async def get_user(db: AsyncSession, user_id: uuid.UUID):
    query = select(User).where(User.id == user_id)
    result = await db.execute(query) # type: ignore
    return result.scalar_one_or_none()


async def get_users(db:AsyncSession, fetch: int = 10):
    query = select(User).order_by(User.id).fetch(fetch)
    result = await db.execute(query)
    return result.scalars().all()

async def create_user(db:AsyncSession, user:CreateUser):
    user_pwd = pwd_context.hash(user.password)
    user = User(email=user.email, password=user_pwd, first_name= user.first_name, last_name = user.last_name) # type: ignore
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def get_user_by_email(db:AsyncSession, user_email: str):
    query = select(User).where(User.email==user_email)
    result = await db.execute(query)
    return result.scalar_one_or_none()
