import uuid

from pydantic import BaseModel


class BaseUser(BaseModel):
    email: str


class CreateUser(BaseUser):
    password: str
    first_name : str
    last_name: str


class User(BaseUser):
    id: uuid.UUID
    first_name : str
    last_name : str

    class Config:
        from_attributes = True