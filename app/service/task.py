from typing import List

from sqlalchemy.orm import Session

from app.models.task import TaskCreate, Task
from app.service.crud import create_task, get_task, update_task


def create_task_db(db: Session, task_data: TaskCreate):
    return create_task(db, task_data)


def get_task_db(db: Session, task_id: int):
    return get_task(db, task_id)


def update_task_db(db: Session, tasks_data: List[Task]):
    for task in tasks_data:
        update_task(db, task.id, task)
