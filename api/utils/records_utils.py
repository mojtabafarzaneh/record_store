import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from data.models.records import Records
from schema.records_schema import CreateRecords


async def create_record(db: AsyncSession, record: CreateRecords):
    record = Records(album_id = record.album_id, record_type = record.record_type) # type: ignore
    db.add(record)
    await db.commit()
    await db.refresh(record)
    return record

async def get_records(db: AsyncSession, fetch: int = 10):
    query = select(Records).order_by(Records.id).fetch(fetch)
    result = await db.execute(query)
    return result.scalars().all()

async def get_record(db: AsyncSession, record_id : uuid.UUID):
    query = select(Records).where(Records.id == record_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()