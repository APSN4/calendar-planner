from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST

from app.models.event import EventCreate
from app.models.user import User, UserCreate, UserId
from app.service.crud import create_user, create_event, get_user, update_user


def create_event_db(db: Session, event_data: EventCreate):
    return create_event(db, event_data)


def get_user_by_id(db: Session, user_data: UserId):
    return get_user(db, user_data.id)


def update_user_db(db: Session, user_id: int, user_data: User):
    update_user(db, user_id, user_data)
