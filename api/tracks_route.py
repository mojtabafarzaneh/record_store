import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.utils.album_utils import get_album
from api.utils.jwt import JWTHandler
from api.utils.tracks_utils import create_track, get_tracks, get_tracks_by_id
from data.db_engine import get_async_db
from data.models.records import Album
from schema.jwt import JWTPayload
from schema.tracks_schema import CreateTrack, Track

tracks_router = APIRouter()

@tracks_router.get("/albums/tracks", response_model=List[Track])
async def read_tracks(
    db: AsyncSession = Depends(get_async_db),
    tocken_data: JWTPayload = Depends(JWTHandler.verify_token)
    ):
    db_tracks = await get_tracks(db = db)
    if db_tracks is None :
        raise HTTPException(404, "no tracks has been found for this album!")
    return db_tracks

@tracks_router.get("/albums/tracks/{track_id}", response_model=Track)
async def read_track( track_id: uuid.UUID,
                     db: AsyncSession = Depends(get_async_db),
                    tocken_data: JWTPayload = Depends(JWTHandler.verify_token)
                    ):
    db_track = await get_tracks_by_id(db=db, track_id= track_id)
    if db_track is None:
        raise HTTPException(404, "the requested track doesn't exists")
    return db_track

@tracks_router.post("/albums/tracks", response_model=Track)
async def insert_track(
    track:CreateTrack,
    db: AsyncSession = Depends(get_async_db),
    tocken_data: JWTPayload = Depends(JWTHandler.verify_token)
    ):
    validate_track = await get_album(db=db, album_id=track.album_id)
    if validate_track is None:
        raise HTTPException(404, "intended album does not exists")

    created_track = await create_track(db=db, track=track)

    return created_track