from sqlalchemy.orm.session import Session
from db import get_db
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from cruds.photo import get_photos_handler, create_photo_handler, delete_photo_handler
# from cruds.firebase_auth import GetCurrentUser
from schemas.photo import BasePhoto, Photo, Photos
from schemas.util import DeleteStatus
from db import models

photos = APIRouter()


@photos.get('/', response_model=Photos)
async def get_photos(user_id: str, tag_ids: str = "", db: Session = Depends(get_db)):
    tag_list = []
    if tag_ids != "":
        tag_list = tag_ids.split(',')
    result = get_photos_handler(user_id, tag_list, db)
    return result


@photos.post('/', response_model=Photo)
async def post_photo(user_id: str, payload: BasePhoto, db: Session = Depends(get_db)):
    result = create_photo_handler(
        db, payload.photo_id, payload.photo_url, payload.tag_ids, user_id)
    return result


@photos.delete('/{tag_id}', response_model=DeleteStatus)
async def delete_photo(user_id: str, tag_id: str = '', db: Session = Depends(get_db)):
    result = delete_photo_handler(db, tag_id, user_id)
    return result
