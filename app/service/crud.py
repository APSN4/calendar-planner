from app.database.db import UserDB, EventDB, TaskDB
from app.models.event import Event
from app.models.task import Task
from app.models.user import User
import json


def create_user(db_session, user: User):
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


def update_user(db_session, user_id: int, user: User):
    db_user = get_user(db_session, user_id)
    if db_user is None:
        return None
    db_user.name = user.name
    db_user.surname = user.surname
    db_user.email = user.email
    db_user.password = user.password
    db_session.commit()
    db_session.refresh(db_user)
    return db_user


def delete_user(db_session, user_id: int):
    db_user = get_user(db_session, user_id)
    if db_user:
        db_session.delete(db_user)
        db_session.commit()
    return db_user


def create_event(db_session, event: Event):
    db_event = EventDB(
        date=event.date,
        time=event.time,
        place=event.place,
        budget=event.budget,
        description=event.description,
        task_list=json.dumps(event.task_list),  # Convert list to JSON string
        progress_bar=event.progress_bar,
        alert=json.dumps(event.alert),  # Convert list to JSON string
        status=event.status
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


def delete_event(db_session, event_id: int):
    db_event = get_event(db_session, event_id)
    if db_event:
        db_session.delete(db_event)
        db_session.commit()
    return db_event


def create_task(db_session, task: Task):
    db_task = TaskDB(
        description=json.dumps(task.description),  # Convert list to JSON string
        completed=task.completed
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
    db_task.description = json.dumps(task.description)
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
