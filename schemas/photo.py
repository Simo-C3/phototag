from pydantic import BaseModel
from datetime import datetime
from .tag import Tag


class BasePhoto(BaseModel):
    photo_id: str
    photo_url: str
    tag_ids: list[str]


class Photo(BaseModel):
    id: str
    photo_id: str
    photo_url: str
    created_at: datetime
    updated_at: datetime
    tags: list[Tag]

    class Config:
        orm_mode = True


class Photos(BaseModel):
    photos: list[Photo]
    total_number: int

    class Config:
        orm_mode = True
