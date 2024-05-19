from app.database.db import UserDB, EventDB, TaskDB, FileDB
from app.models.event import Event, EventCreate, EventUpdate, UploadFileEvent
from app.models.task import Task, TaskCreate
from app.models.user import User, UserCreate
import json


def create_user(db_session, user: UserCreate):
    db_user = UserDB(
        name=user.name,
        surname=user.surname,
        email=user.email,
        password=user.password
    )
    db_session.add(db_user)
    db_session.commit()
    db_session.refresh(db_user)
    return db_user


def get_user(db_session, user_id: int):
    return db_session.query(UserDB).filter(UserDB.id == user_id).first()


def get_user_by_email(db_session, user_email: str):
    return db_session.query(UserDB).filter(UserDB.email == user_email).first()


def update_user(db_session, user_id: int, user: User):
    db_user = get_user(db_session, user_id)
    if db_user is None:
        return None
    print(user)
    db_user.name = user.name
    db_user.surname = user.surname
    db_user.email = user.email
    db_user.password = user.password
    db_user.event_list = user.event_list
    db_session.commit()
    db_session.refresh(db_user)
    return db_user


def delete_user(db_session, user_id: int):
    db_user = get_user(db_session, user_id)
    if db_user:
        db_session.delete(db_user)
        db_session.commit()
    return db_user


def create_event(db_session, event: EventCreate):
    db_event = EventDB(
        date=event.date,
        time=event.time,
        place=event.place,
        budget=event.budget,
        description=event.description,
        alert=event.alert,
    )
    db_session.add(db_event)
    db_session.commit()
    db_session.refresh(db_event)
    return db_event


def get_event(db_session, event_id: int):
    return db_session.query(EventDB).filter(EventDB.id == event_id).first()


def update_event(db_session, event_id: int, event: Event):
    db_event = get_event(db_session, event_id)
    if db_event is None:
        return None
    db_event.date = event.date
    db_event.time = event.time
    db_event.place = event.place
    db_event.budget = event.budget
    db_event.description = event.description
    db_event.task_list = json.dumps(event.task_list)
    db_event.progress_bar = event.progress_bar
    db_event.alert = json.dumps(event.alert)
    db_event.status = event.status
    db_session.commit()
    db_session.refresh(db_event)
    return db_event


def update_event_exist(db_session, event_id: int, event: EventCreate):
    db_event = get_event(db_session, event_id)
    if db_event is None:
        return None
    db_event.date = event.date
    db_event.time = event.time
    db_event.place = event.place
    db_event.budget = event.budget
    db_event.description = event.description
    db_event.alert = event.alert
    db_session.commit()
    db_session.refresh(db_event)
    return db_event


def update_event_exist_file(db_session, event_id: int, event: UploadFileEvent):
    db_event = get_event(db_session, event_id)
    if db_event is None:
        return None
    db_event.files = json.dumps(event.files)
    db_session.commit()
    db_session.refresh(db_event)
    return db_event


def get_event_exist_file(db_session, file_id: int):
    return get_file(db_session, file_id)


def update_event_tasks_list(db_session, event_id: int, event: EventUpdate):
    db_event = get_event(db_session, event_id)
    if db_event is None:
        return None
    db_event.task_list = json.dumps(event.task_list)
    db_session.commit()
    db_session.refresh(db_event)
    return db_event


def delete_event(db_session, event_id: int):
    db_event = get_event(db_session, event_id)
    if db_event:
        db_session.delete(db_event)
        db_session.commit()
    return db_event


def create_task(db_session, task: TaskCreate):
    db_task = TaskDB(
        description=task.description,
    )
    db_session.add(db_task)
    db_session.commit()
    db_session.refresh(db_task)
    return db_task


def get_task(db_session, task_id: int):
    return db_session.query(TaskDB).filter(TaskDB.id == task_id).first()


def update_task(db_session, task_id: int, task: Task):
    db_task = get_task(db_session, task_id)
    if db_task is None:
        return None
    db_task.description = task.description
    db_task.completed = task.completed
    db_session.commit()
    db_session.refresh(db_task)
    return db_task


def delete_task(db_session, task_id: int):
    db_task = get_task(db_session, task_id)
    if db_task:
        db_session.delete(db_task)
        db_session.commit()
    return db_task


# Delete
def delete_task(db_session, task_id: int):
    db_task = get_task(db_session, task_id)
    if db_task:
        db_session.delete(db_task)
        db_session.commit()
        return db_task
    return None


# Create
def create_file(db_session, content: bytes, filename: str):
    db_file = FileDB(content=content, filename=filename)
    db_session.add(db_file)
    db_session.commit()
    db_session.refresh(db_file)
    return db_file


# Read
def get_file(db_session, file_id: int):
    return db_session.query(FileDB).filter(FileDB.id == file_id).first()


# Update
def update_file(db_session, file_id: int, new_content: bytes, new_filename: str):
    db_file = db_session.query(FileDB).filter(FileDB.id == file_id).first()
    if db_file:
        db_file.content = new_content
        db_file.filename = new_filename
        db_session.commit()
        db_session.refresh(db_file)
        return db_file
    return None


# Delete
def delete_file(db_session, file_id: int):
    db_file = db_session.query(FileDB).filter(FileDB.id == file_id).first()
    if db_file:
        db_session.delete(db_file)
        db_session.commit()
        return True
    return False

