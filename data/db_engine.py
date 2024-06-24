from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (AsyncAttrs, AsyncSession,
                                    create_async_engine)
from sqlalchemy.orm import (DeclarativeBase, MappedAsDataclass,
                            declarative_base, sessionmaker)

ASYNC_DATABASE_URL = "postgresql+asyncpg://postgres:mojtaba7878@localhost:5432/record_store"

engine = create_async_engine(ASYNC_DATABASE_URL)

AsyncLocalSession = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False) # type: ignore


class Base(DeclarativeBase, MappedAsDataclass, AsyncAttrs):
    pass

@asynccontextmanager
async def get_async_session():
    session = AsyncLocalSession()
    try:
        yield session
    except Exception as e:
        print(e)
        await session.rollback() # type: ignore
    finally:
        await session.close() # type: ignore


def async_session(func):
    async def wrapper(*args, **kwargs):
        async with get_async_session() as session:
            return await func(session, *args, **kwargs)
    return wrapper
