from contextlib import asynccontextmanager

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import (AsyncAttrs, AsyncSession,
                                    create_async_engine)
from sqlalchemy.orm import (DeclarativeBase, MappedAsDataclass,
                            declarative_base, sessionmaker)

ASYNC_DATABASE_URL = "postgresql+asyncpg://postgres:mojtaba7878@localhost:5432/record_store"

engine = create_async_engine(ASYNC_DATABASE_URL)

AsyncLocalSession = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False) # type: ignore

metadata = MetaData()

class Base(DeclarativeBase, AsyncAttrs):
    pass

async def get_async_db():
    async with AsyncLocalSession() as db: # type: ignore
        yield db
        await db.commit()