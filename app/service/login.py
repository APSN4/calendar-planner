from sqlalchemy.orm import Session

from app.models.user import UserLogin
from app.service.crud import create_user, get_user, get_user_by_email


def login_service(db: Session, user_data: UserLogin):
    return get_user_by_email(db, user_data.email)
