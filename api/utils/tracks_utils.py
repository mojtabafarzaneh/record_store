import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from data.models.records import Tracks
from schema.tracks_schema import CreateTrack


async def get_tracks(db: AsyncSession, fetch:int = 10):
    query = select(Tracks).order_by(Tracks.id).fetch(fetch)
    result = await db.execute(query)
    return result.scalars().all()

async def get_tracks_by_id(db: AsyncSession, track_id: uuid.UUID):
    query = select(Tracks).where(Tracks.id == track_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def create_track(db: AsyncSession, track: CreateTrack):
    track = Tracks(album_id = track.album_id, title = track.title) # type: ignore
    db.add(track)
    await db.commit()
    await db.refresh(track)
    return track
