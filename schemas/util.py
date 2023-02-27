from pydantic import BaseModel
from datetime import datetime


class DeleteStatus(BaseModel):
    status: str

    class Config:
        orm_mode = True
