import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.utils.user_utils import (create_user, get_user, get_user_by_email,
                                  get_users)
from data.db_engine import get_async_db
from schema.user_schema import CreateUser, User

router = APIRouter()


@router.get("/users/{user_id}", response_model=User)
async def read_user(user_id: uuid.UUID, db: AsyncSession = Depends(get_async_db)):
    db_user = await get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(404, "user not found")
    return db_user


@router.get("/users", status_code=200, response_model=List[User])
async def read_users(db:AsyncSession = Depends(get_async_db)):
    db_user = await get_users(db=db, fetch=10)
    if db_user is None:
        raise HTTPException(404, "no user has been found")
    return db_user

@router.post("/users", response_model=User)
async def create_new_user(user: CreateUser, db: AsyncSession=Depends(get_async_db)):
    validate_user = await get_user_by_email(db=db, user_email=user.email)
    if validate_user:
        raise HTTPException(status_code=400, detail="user already exists")
    user = await create_user(db=db, user=user) # type: ignore
    return user

