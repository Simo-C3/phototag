from pydantic import BaseModel


class User(BaseModel):
    uid: str

    class Config:
        orm_mode = True
