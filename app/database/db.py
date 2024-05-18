import json

from sqlalchemy import create_engine, Column, String, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.constant.constant import DB_USER, DB_PASSWORD

SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@localhost:5432/postgres"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    surname = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    event_list = Column(String)

    def __init__(self, name, surname, email, password, event_list=None):
        self.name = name
        self.surname = surname
        self.email = email
        self.password = password
        if event_list is None:
            self.event_list = "[]"  # По умолчанию список событий пустой, представленный в виде JSON строки
        else:
            self.event_list = json.dumps(event_list)


class EventDB(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, index=True)
    time = Column(String, index=True)
    place = Column(String, index=True)
    budget = Column(Integer)
    description = Column(String)
    task_list = Column(String)  # We'll store the task list as a JSON string
    progress_bar = Column(Integer)
    alert = Column(String)
    status = Column(Integer)

    def __init__(self, date, time, place, budget, description, task_list=None, progress_bar=0, alert=None, status=0):
        self.date = date
        self.time = time
        self.place = place
        self.budget = budget
        self.description = description
        self.task_list = json.dumps(task_list) if task_list is not None else "[]"
        self.progress_bar = progress_bar
        self.alert = alert
        self.status = status


class TaskDB(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)  # We'll store the description list as a JSON string
    completed = Column(Boolean, default=False)

    def __init__(self, description, completed=False):
        self.description = json.dumps(description, ensure_ascii=False) if description is not None else "[]"
        self.completed = completed
