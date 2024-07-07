import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.utils.auth_utils import auth_user
from api.utils.jwt import JWTHandler
from api.utils.secrets import pwd_context
from data.db_engine import get_async_db
from schema.jwt import JWTResponsePayload
from schema.user_schema import AuthUser

auth_router = APIRouter()

@auth_router.post("/auth", response_model=JWTResponsePayload, status_code=200)
async def auth(user: AuthUser, db: AsyncSession = Depends(get_async_db)):
    db_response = await auth_user(db=db, user_email=user.email) # type: ignore
    if db_response is None:
        raise HTTPException(400, "email does not match")
    if not pwd_context.verify(user.password, db_response.password): # type: ignore
        raise HTTPException(400, "password does not match")


    return JWTHandler.generate(db_response.email)
