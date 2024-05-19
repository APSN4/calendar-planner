from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST

from app.models.event import EventCreate, EventGet, EventUpdate, UploadFileEvent, GetFileEvent
from app.models.user import User, UserCreate, UserId
from app.service.crud import create_user, create_event, get_user, update_user, get_event, update_event_exist, \
    update_event_exist_file


def create_event_db(db: Session, event_data: EventCreate):
    return create_event(db, event_data)


def get_event_db(db: Session, event_data: EventGet):
    return get_event(db, event_data.id)


def update_event_db(db: Session, event_id: int, user_data: EventCreate):
    return update_event_exist(db, event_id, user_data)


def update_event_exist_file_db(db: Session, event_id: int, event_data: UploadFileEvent):
    return update_event_exist_file(db, event_id, event_data)


def get_event_exist_file_db(db: Session, event_id: int, event_data: GetFileEvent):
    return update_event_exist_file(db, event_id, event_data)


def get_user_by_id(db: Session, user_data: UserId):
    return get_user(db, user_data.id)


def update_user_db(db: Session, user_id: int, user_data: User):
    print(user_data.email)
    return update_user(db, user_id, user_data)


def parse_pg_array(pg_array_str):
    # Удаляем фигурные скобки и разделяем по запятой
    if pg_array_str.startswith('{') and pg_array_str.endswith('}'):
        pg_array_str = pg_array_str[1:-1]
    if pg_array_str:
        return list(map(int, pg_array_str.split(',')))
    return []
