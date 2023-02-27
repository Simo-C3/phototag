from pydantic import BaseModel
from datetime import datetime


class BaseTag(BaseModel):
    name: str


class Tag(BaseTag):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class Tags(BaseModel):
    tags: list[Tag]
    total_number: int

    class Config:
        orm_mode = True
