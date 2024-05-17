from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST

from app.models.user import User, UserCreate
from app.service.crud import create_user


def register(db: Session, user_data: UserCreate):
    create_user(db, user_data)
