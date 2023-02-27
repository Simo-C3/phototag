from fastapi import HTTPException
from db import models
from sqlalchemy.orm.session import Session
from schemas.tag import Tag, Tags
from schemas.util import DeleteStatus


def create_tag_handler(db: Session, name: str, user_id: str) -> Tag:
    if name == "":
        raise HTTPException(status_code=400, detail="Name is empty")

    result_by_name = db.query(models.Tags).filter(
        models.Tags.name == name).first()
    if result_by_name != None:
        raise HTTPException(status_code=400, detail="The tag is exist")

    tag_orm = models.Tags(name=name, user_uid=user_id)
    db.add(tag_orm)
    db.commit()
    db.refresh(tag_orm)

    tag = Tag.from_orm(tag_orm)

    return tag


def get_tags_handler(user_id: str, db: Session) -> Tags:
    tag_orm = db.query(models.Tags).filter(
        models.Tags.user_uid == user_id).order_by(models.Tags.name)

    tag_orm = tag_orm.all()
    tag_list = list(map(Tag.from_orm, tag_orm))

    tags = Tags(tags=tag_list, total_number=len(tag_list))

    return tags


def delete_tag_handler(db: Session, tag_id: str, user_id: str) -> DeleteStatus:
    tag_orm = db.query(models.Tags).filter(models.Tags.id == tag_id).filter(
        models.Tags.user_uid == user_id).first()
    if tag_orm == None:
        raise HTTPException(status_code=400, detail="The tag is not exist")

    db.delete(tag_orm)
    db.commit()

    result = DeleteStatus(status="OK")

    return result
