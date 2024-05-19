import json
from typing import List

from fastapi import APIRouter, Request, Form, Depends, Cookie, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from app.database.db import get_db
from app.models.event import EventCreate, EventDelete, EventGet, EventUpdate, EventUpdatePost
from app.models.task import TaskCreate, Task
from app.models.user import User, UserCreate, UserId
from app.service.crud import delete_event, update_event_tasks_list
from app.service.event import create_event_db, get_user_by_id, update_user_db, parse_pg_array, get_event_db, \
    update_event_db
from app.service.md5 import calculate_md5
from app.service.register import register
from fastapi.responses import RedirectResponse

from app.service.task import create_task_db, update_task_db

router = APIRouter()
templates = Jinja2Templates(directory="app/frontend")


def verify_user_id(user_id: str = Cookie(None)):
    """
    Verify the token from the cookie.
    """
    if user_id is None:
        return RedirectResponse(url="/")
    return user_id


@router.post("/")
async def event_create(user_id: str = Depends(verify_user_id), date: str = Form(...), time: str = Form(...),
                       place: str = Form(...), budget: str = Form(...), description: str = Form(...),
                       reminder_time: str = Form(...)):
    event = EventCreate(date=date, time=time, place=place, budget=budget, description=description, alert=reminder_time)
    new_event = create_event_db(next(get_db()), event)
    try:
        user_id = user_id.title()
    except Exception as e:
        return RedirectResponse(url="/")
    user = UserId(id=user_id)
    user_bd = get_user_by_id(next(get_db()), user)
    try:
        event_list = json.loads(str(parse_pg_array(user_bd.event_list)))
    except Exception as e:
        event_list = []
    event_list.append(new_event.id)
    user_bd.event_list = event_list
    update_user_db(next(get_db()), int(user_id), user_bd)

    response_redirect = RedirectResponse(url="/", status_code=303)
    return response_redirect


@router.post("/update")
async def event_create(event_data: EventUpdatePost):
    event = EventCreate(date=event_data.date, time=event_data.time, place=event_data.place, budget=event_data.budget, description=event_data.description, alert=str(event_data.alert))
    event_update = update_event_db(next(get_db()), int(event_data.event_id), event)

    response_redirect = RedirectResponse(url="/", status_code=303)
    return response_redirect


class UpdateTasksRequest(BaseModel):
    event_id: int
    checkboxes: List[Task]


@router.post("/task/update")
async def update_tasks(request: UpdateTasksRequest):
    try:
        update_task_db(next(get_db()), request.checkboxes)
        response_redirect = RedirectResponse(url="/", status_code=303)
        return response_redirect
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/task")
async def task_create(user_id: str = Depends(verify_user_id), description: str = Form(...), event_id: str = Form(...)):
    task = TaskCreate(description=description)
    new_task = create_task_db(next(get_db()), task)
    event_local = EventGet(id=event_id)
    event = get_event_db(next(get_db()), event_local)
    print(event.task_list)
    tasks_list = json.loads(str(event.task_list))
    tasks_list.append(new_task.id)
    event.task_list = tasks_list
    update_event_tasks_list(next(get_db()), int(event_id), event)

    response_redirect = RedirectResponse(url="/", status_code=303)
    return response_redirect


@router.post("/delete")
async def event_delete(user_id: str = Depends(verify_user_id), event_id: str = Form(...)):
    event = EventDelete(id=event_id)

    try:
        user_id = user_id.title()
    except Exception as e:
        return RedirectResponse(url="/")

    user = UserId(id=user_id)
    user_bd = get_user_by_id(next(get_db()), user)
    event_list = json.loads(str(parse_pg_array(user_bd.event_list)))
    event_list.remove(event.id)
    user_bd.event_list = event_list
    update_user_db(next(get_db()), int(user_id), user_bd)
    delete_event(next(get_db()), int(event.id))

    response_redirect = RedirectResponse(url="/", status_code=303)
    return response_redirect
