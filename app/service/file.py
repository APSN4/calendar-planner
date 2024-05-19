from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST

from app.models.event import EventCreate, EventGet, EventUpdate, UploadFileEvent, GetFileEvent
from app.models.user import User, UserCreate, UserId
from app.service.crud import get_file, create_file


def get_file_db(db: Session, file_id: int):
    return get_file(db, file_id)


def create_file_db(db: Session, content: bytes, filename: str):
    return create_file(db, content, filename)
