from sqlalchemy.orm.session import Session
from db import get_db
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from cruds.tag import get_tags_handler, create_tag_handler, delete_tag_handler
# from cruds.firebase_auth import GetCurrentUser
from schemas.tag import BaseTag, Tag, Tags
from schemas.util import DeleteStatus
from db import models

tags = APIRouter()


@tags.get('/', response_model=Tags)
async def get_tags(user_id: str, db: Session = Depends(get_db)):
    result = get_tags_handler(user_id, db)
    return result


@tags.post('/', response_model=Tag)
async def post_tag(user_id: str, payload: BaseTag, db: Session = Depends(get_db)):
    result = create_tag_handler(db, payload.name, user_id)
    return result


@tags.delete('/{tag_id}', response_model=DeleteStatus)
async def delete_tag(user_id: str, tag_id: str = '', db: Session = Depends(get_db)):
    result = delete_tag_handler(db, tag_id, user_id)
    return result
