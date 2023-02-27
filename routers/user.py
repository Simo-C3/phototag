from sqlalchemy.orm.session import Session
from db import get_db
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from cruds.user import create_user_handler, delete_user_handler
from schemas.user import User
from schemas.util import DeleteStatus

users = APIRouter()


@users.post('/', response_model=User)
async def post_user(payload: User, db: Session = Depends(get_db)):
    # if (payload.google_uid != user.google_uid):
    #     raise HTTPException(
    #         status_code=400,
    #         detail="ID is incorrect"
    #     )
    result = create_user_handler(db, payload.uid)
    return result


@users.delete('/{user_id}', response_model=DeleteStatus)
async def delete_user(user_id: str = "", db: Session = Depends(get_db)):
    result = delete_user_handler(db, user_id)
    return result
