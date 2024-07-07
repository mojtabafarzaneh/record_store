import uuid
from calendar import c
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.utils.jwt import JWTHandler
from api.utils.records_utils import get_record
from api.utils.shoping_card_utils import create_card, get_card, get_cards
from api.utils.user_utils import get_user
from data.db_engine import get_async_db
from schema.jwt import JWTPayload
from schema.shopin_card_schema import Card, CreateCard

card_router = APIRouter()


@card_router.post("/card/{user_id}/{record_id}", response_model=Card, status_code=201)
async def insert_card(card : CreateCard,
                      user_id: uuid.UUID,
                      record_id: uuid.UUID,
                      db: AsyncSession = Depends(get_async_db),
                      tocken_data: JWTPayload = Depends(JWTHandler.verify_token)
                      ):

    validate_user = await get_user(db=db, user_id=user_id)
    if validate_user is None :
        raise HTTPException(404, "user not found")
    validate_record = await get_record(db=db, record_id=record_id) # type: ignore
    if validate_record is None:
        raise HTTPException(404, "record not found")
    inserted = await create_card(
        db=db,
        card= card,
        record_id= record_id,
        user_id=user_id
    )
    return inserted


@card_router.get("/card/{card_id}", response_model=Card, status_code=200)
async def read_card(card_id : uuid.UUID,
                    db:AsyncSession = Depends(get_async_db),
                    tocken_data: JWTPayload = Depends(JWTHandler.verify_token)
                    ):
    db_response = await get_card(db=db, card_id=card_id)
    if db_response is None:
        raise HTTPException(404, "didn't found the card id")
    return db_response

@card_router.get("/card", response_model=List[Card], status_code=200)
async def read_cards(db: AsyncSession = Depends(get_async_db), tocken_data: JWTPayload = Depends(JWTHandler.verify_token)):
    db_response = await get_cards(db=db)
    if db_response is None:
        raise HTTPException(404, "there ain't any cards in here!")
    return db_response