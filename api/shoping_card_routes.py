import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.utils.records_utils import get_record
from api.utils.shoping_card_utils import create_card
from api.utils.user_utils import get_user
from data.db_engine import get_async_db
from schema.shopin_card_schema import Card, CreateCard

card_router = APIRouter()


#TODO:make sure you don't need to pass user or record id in json fields
#TODO:remanage the database with foriegn keys
@card_router.post("/card/{user_id}/{record_id}", response_model=Card, status_code=201)
async def insert_card(card : CreateCard, db: AsyncSession = Depends(get_async_db)):
    validate_user = await get_user(db=db, user_id=card.user_id)
    if validate_user is None :
        raise HTTPException(404, "user not found")
    validate_record = await get_record(db=db, record_id=card.record_id) # type: ignore
    if validate_record is None:
        raise HTTPException(404, "record not found")
    inserted = await create_card(
        db=db,
        card= card
    )
    return inserted