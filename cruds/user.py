from fastapi import HTTPException
from db import models
from sqlalchemy.orm.session import Session
from schemas.user import User
from schemas.util import DeleteStatus


def create_user_handler(db: Session, user_id: str) -> User:
    if user_id == "":
        raise HTTPException(status_code=400, detail="Name is empty")

    user_orm = models.Users(uid=user_id)
    print(user_orm)
    db.add(user_orm)
    db.commit()
    db.refresh(user_orm)

    user = User.from_orm(user_orm)

    return user


def delete_user_handler(db: Session, user_id: str) -> DeleteStatus:
    user_orm = db.query(models.Users).filter(
        models.Users.id == user_id).first()
    if user_orm == None:
        raise HTTPException(status_code=400, detail="The user is not exist")

    db.delete(user_orm)
    db.commit()

    result = DeleteStatus(status="OK")

    return result
