from pydantic import BaseModel


class JWTResponsePayload(BaseModel):
    access: str

class JWTPayload(BaseModel):
    email: str
    exp: int
