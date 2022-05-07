from pydantic import BaseModel


class History(BaseModel):
    channel_id: str
    history: list[str] = []


class UserBase(BaseModel):
    username: str


class User(UserBase):
    id: str
