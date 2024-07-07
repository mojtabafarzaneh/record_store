import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.utils.album_utils import create_album, get_album, get_albums
from api.utils.jwt import JWTHandler
from data.db_engine import get_async_db
from schema.albums_schema import Album, CreateAlbum
from schema.jwt import JWTPayload

album_router = APIRouter()

@album_router.get("/albums/{album_id}", response_model=Album, status_code=200)
async def read_album(album_id : uuid.UUID,
                     db: AsyncSession = Depends(get_async_db),
                     tocken_data: JWTPayload = Depends(JWTHandler.verify_token)):
    reads = await get_album(db=db, album_id=album_id)
    if reads is None:
        raise HTTPException(404, "intended album does not exists")

    return reads

@album_router.get("/album", response_model=List[Album], status_code=200) # type: ignore
async def read_albums(db:AsyncSession = Depends(get_async_db), tocken_data: JWTPayload = Depends(JWTHandler.verify_token)):
    reading_albums = await get_albums(db=db)
    if reading_albums is None:
        raise HTTPException(404, "There ain't no album to return")

    return reading_albums


@album_router.post("/album", response_model=Album, status_code=201)
async def insert_album(album : CreateAlbum,
                       db: AsyncSession = Depends(get_async_db),
                       tocken_data: JWTPayload = Depends(JWTHandler.verify_token)):
    created_album = await create_album(db=db, album=album)
    return created_album
