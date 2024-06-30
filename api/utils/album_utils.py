import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from data.models.records import Album
from schema.albums_schema import CreateAlbum


async def get_album(db:AsyncSession, album_id : uuid.UUID):
    query = select(Album).where(Album.id == album_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def get_albums(db: AsyncSession, fetch: int = 10):
    query = select(Album).order_by(Album.id).fetch(fetch)
    result = await db.execute(query)
    return result.scalars().all()

async def create_album(db:AsyncSession, album:CreateAlbum):
    album = Album(genre = album.genre, artist = album.artist, title=album.title) # type: ignore
    db.add(album)
    await db.commit()
    await db.refresh(album)
    return album