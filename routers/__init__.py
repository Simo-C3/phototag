from fastapi import APIRouter
from .user import users
from .tag import tags
from .photo import photos

router = APIRouter()

router.include_router(users, prefix='/users', tags=['users'])
router.include_router(tags, prefix='/tags', tags=['tags'])
router.include_router(photos, prefix='/photos', tags=['photos'])
