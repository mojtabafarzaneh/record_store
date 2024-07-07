import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.utils.album_utils import get_album
from api.utils.jwt import JWTHandler
from api.utils.records_utils import create_record, get_record, get_records
from data.db_engine import get_async_db
from schema.jwt import JWTPayload
from schema.records_schema import CreateRecords, Records

records_router = APIRouter()

@records_router.post("/records",response_model=Records, status_code=201)
async def insert_records(records : CreateRecords,
                         db: AsyncSession = Depends(get_async_db),
                         tocken_data: JWTPayload = Depends(JWTHandler.verify_token)):
    album_id = await get_album(db=db, album_id=records.album_id) # type: ignore
    if album_id is None:
        raise HTTPException(404, "requested album does not exists")

    inserted = await create_record(db = db, record=records)

    return inserted

@records_router.get("/records", response_model=List[Records], status_code=200)
async def read_records(db: AsyncSession = Depends(get_async_db), tocken_data: JWTPayload = Depends(JWTHandler.verify_token)):
    db_response = await get_records(db=db)
    if db_response is None :
        raise HTTPException(404, "no records has been found")
    return db_response

@records_router.get("/records/{records_id}", response_model=Records, status_code=200)
async def read_record(records_id: uuid.UUID,
                      db: AsyncSession = Depends(get_async_db),
                      tocken_data: JWTPayload = Depends(JWTHandler.verify_token)):
    db_response = await get_record(db=db, record_id=records_id)
    if db_response is None:
        raise HTTPException(404, "this record does not exists")
    return db_response