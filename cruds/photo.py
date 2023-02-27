from fastapi import HTTPException
from db import models
from sqlalchemy.orm.session import Session
from schemas.photo import BasePhoto, Photo, Photos
from schemas.util import DeleteStatus
from sqlalchemy import desc, func


def create_photo_handler(db: Session, photo_id: str, photo_url: str, tag_ids: list[str], user_id: str) -> Photo:
    if photo_id == "":
        raise HTTPException(status_code=400, detail="id is empty")
    if photo_url == "":
        raise HTTPException(status_code=400, detail="url is empty")

    photo_orm = models.Photos(
        user_uid=user_id, photo_id=photo_id, photo_url=photo_url)
    db.add(photo_orm)
    db.commit()
    db.refresh(photo_orm)

    for tag_id in tag_ids:
        tagging_orm = models.Tagging(photo_id=photo_orm.id, tag_id=tag_id)
        db.add(tagging_orm)
        db.commit()

    db.refresh(photo_orm)

    photo = Photo.from_orm(photo_orm)
    return photo


def get_photos_handler(user_id: str, tag_ids: list[str], db: Session) -> Photos:
    photo_orm = db.query(models.Photos).filter(
        models.Photos.user_uid == user_id)

    if len(tag_ids) > 0:
        photo_orm = photo_orm.filter(models.Tagging.tag_id.in_(tag_ids)).filter(
            models.Tagging.photo_id == models.Photos.id
        )
        photo_orm = photo_orm.group_by(models.Photos.id).having(
            func.count(models.Photos.id) == len(tag_ids)
        )

    photo_orm = photo_orm.order_by(models.Photos.created_at).all()
    photo_list = list(map(Photo.from_orm, photo_orm))

    photos = Photos(photos=photo_list, total_number=len(photo_list))

    return photos


def delete_photo_handler(db: Session, photo_id: str, user_id: str) -> DeleteStatus:
    photo_orm = db.query(models.Photos).filter(models.Photos.id == photo_id).filter(
        models.Photos.user_uid == user_id).first()
    if photo_orm == None:
        raise HTTPException(status_code=400, detail="The photo is not exist")

    db.delete(photo_orm)
    db.commit()

    result = DeleteStatus(status="OK")

    return result
