from fastapi import FastAPI

from api.user_routes import router as user_routes
from data.db_engine import Base, engine
from data.models import records, user

app = FastAPI(
    title="FastAPI record_store",
    description= "api for selling vynil records",
    version="0.1.0",
    license_info={
        "name":"MIT"
    }
)

@app.on_event("startup")
async def init_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(user_routes)
