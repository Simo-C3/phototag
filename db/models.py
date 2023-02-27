from typing import Any
from sqlalchemy import Column as Col, String, Enum, ForeignKey, DateTime, Boolean, Integer, Text, JSON
from uuid import uuid4
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import relationship
import enum
import datetime
from sqlalchemy.sql.functions import func


class Column(Col):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('nullable', False)
        super().__init__(*args, **kwargs)


def generate_uuid():
    return str(uuid4())


@as_declarative()
class Base:
    id: Any
    __name__: Any

    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()


class Users(Base):

    __tablename__ = "users"

    uid = Column(String(length=255), primary_key=True)


class Tagging(Base):

    __tablename__ = "taggings"

    photo_id = Column(String(length=255), ForeignKey(
        "photos.id"), primary_key=True)
    tag_id = Column(String(length=255), ForeignKey(
        "tags.id"), primary_key=True)


class Tags(Base):

    __tablename__ = "tags"

    id = Column(String(length=255), primary_key=True, default=generate_uuid)
    user_uid = Column(String(length=255), ForeignKey('users.uid'))
    name = Column(String(length=255))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    photos = relationship(
        "Photos", secondary=Tagging.__tablename__, back_populates="tags")


class Photos(Base):

    __tablename__ = "photos"

    id = Column(String(length=255), primary_key=True, default=generate_uuid)
    user_uid = Column(String(length=255), ForeignKey('users.uid'))
    photo_id = Column(String(length=255))
    photo_url = Column(String(length=255))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    tags = relationship(
        "Tags", secondary=Tagging.__tablename__, back_populates="photos")
