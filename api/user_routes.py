import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.utils.user_utils import get_user
from data.db_engine import get_async_db
from schema.user_schema import User

router = APIRouter()


@router.get("/users/{user_id}", response_model=User)
async def read_user(user_id: uuid.UUID, db: AsyncSession = Depends(get_async_db)):
    db_user = await get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(404, "user not found")
    return db_user

