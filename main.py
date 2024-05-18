import json
import logging
from typing import List, Dict

from fastapi import FastAPI, Request, Cookie, Depends, Response

from app.database.db import Base, engine, get_db, TaskDB
from app.models.user import UserId
from app.routers import items, users, registration, login, event

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from app.routers.event import verify_user_id
from app.service.crud import get_event
from app.service.event import get_user_by_id, parse_pg_array
from app.service.task import get_task_db

"""

Запуск производится командой: fastapi run, либо uvicorn main:app --log-level debug
Переход осуществляется по локальному IP в сети. [win cmd: ipconfig]

"""

app = FastAPI()
templates = Jinja2Templates(directory="app/frontend")

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)


def verify_token(token: str = Cookie(None)):
    """
    Verify the token from the cookie.
    """
    if token is None:
        return RedirectResponse(url="/login")
    return token


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request, token: str = Depends(verify_token), user_id: str = Depends(verify_user_id)):
    try:
        cookie = token.title()
    except Exception as e:
        return RedirectResponse(url="/login")

    try:
        user_id = user_id.title()
    except Exception as e:
        return RedirectResponse(url="/")
    user = UserId(id=user_id)
    user_bd = get_user_by_id(next(get_db()), user)
    event_list = json.loads(str(parse_pg_array(user_bd.event_list)))
    events_entities = []
    for event_id in event_list:
        entity = get_event(next(get_db()), event_id)
        events_entities.append(entity)

    scheme_entities_list = [
        {
            "event_id": event_entity.id,
            "date": event_entity.date,
            "time": event_entity.time,
            "place": event_entity.place,
            "budget": event_entity.budget,
            "description": event_entity.description,
            "reminder_time": event_entity.alert,
            "tasks": get_tasks_for_event(next(get_db()), event_entity.task_list)
        }
        for event_entity in events_entities
    ]
    print(scheme_entities_list)

    return templates.TemplateResponse(
        request=request, name="index.html", context={"events": scheme_entities_list}
    )


def get_tasks_for_event(db_session, task_list: str) -> List[Dict[str, any]]:
    tasks_list = json.loads(task_list)
    tasks = []
    for task_id in tasks_list:
        task = get_task_db(db_session, task_id)
        tasks.append({"description": task.description, "completed": str(task.completed).lower()})
    return tasks


@app.post("/exit")
async def exit_user():
    response_redirect = RedirectResponse(url="/login", status_code=303)
    response_redirect.delete_cookie(key="token")
    response_redirect.delete_cookie(key="user_id")
    return response_redirect


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


app.include_router(items.router, prefix="/api/items")
app.include_router(users.router, prefix="/api/users")
app.include_router(registration.router, prefix="/register")
app.include_router(login.router, prefix="/login")
app.include_router(event.router, prefix="/event")
