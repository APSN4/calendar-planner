import json
import logging
from typing import List, Dict

from fastapi import FastAPI, Request, Cookie, Depends, Query

from fastapi.responses import JSONResponse
from fuzzywuzzy import process
from sqlalchemy.orm import Session

from app.database.db import Base, engine, get_db, TaskDB
from app.models.user import UserId
from app.routers import registration, login, event

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from app.routers.event import verify_user_id
from app.service.crud import get_event
from app.service.event import get_user_by_id, parse_pg_array
from app.service.file import get_file_db
from app.service.task import get_task_db

"""

Запуск производится командой: fastapi run, либо uvicorn main:app --log-level debug
Переход осуществляется по локальному IP в сети. [win cmd: ipconfig]

"""

app = FastAPI()
templates = Jinja2Templates(directory="app/frontend")

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

data_search = []


def verify_token(token: str = Cookie(None)):
    """
    Verify the token from the cookie.
    """
    if token is None:
        return RedirectResponse(url="/login")
    return token


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request, token: str = Depends(verify_token), user_id: str = Depends(verify_user_id)):
    global data_search
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
    try:
        event_list = json.loads(str(parse_pg_array(user_bd.event_list)))
    except Exception as e:
        event_list = []
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
            "tasks": get_tasks_for_event(next(get_db()), event_entity.task_list),
            "files": get_files_for_event(event_entity.files)
        }
        for event_entity in events_entities
    ]
    print(scheme_entities_list)
    data_search = scheme_entities_list

    return templates.TemplateResponse(
        request=request, name="index.html", context={"events": scheme_entities_list}
    )


def get_files_for_event(file_ids_str):
    try:
        # Преобразуем строку с массивом чисел в список
        file_ids = [int(id_str) for id_str in file_ids_str[1:-1].split(', ')]

        # Используем генератор списка для создания списка объектов файлов
        return [
            {
                "id": file_db.id,
                "filename": file_db.filename
            }
            for file_id in file_ids
            if (file_db := get_file_db(next(get_db()), file_id))
        ]
    except Exception as e:
        print(e)
        return []


def get_tasks_for_event(db_session: Session, task_list: str) -> List[Dict[str, any]]:
    tasks_list = json.loads(task_list)
    tasks = []
    for task_id in tasks_list:
        task = get_task_db(db_session, task_id)
        tasks.append({"id": task.id, "description": task.description, "completed": str(task.completed).lower()})
    return tasks


@app.post("/exit")
async def exit_user():
    response_redirect = RedirectResponse(url="/login", status_code=303)
    response_redirect.delete_cookie(key="token")
    response_redirect.delete_cookie(key="user_id")
    return response_redirect


@app.get("/search")
async def search(q: str = Query(..., min_length=1)):
    # Подготавливаем данные для поиска
    combined_search_data = [
        (
            f"{event_search['date']} {event_search['time']} {event_search['place']} {event_search['budget']} {event_search['description']} {event_search['reminder_time']}",
            event_search
        )
        for event_search in data_search
    ]

    # Выполняем поиск
    results = process.extract(q, combined_search_data, limit=5)

    # Извлекаем результаты
    matched_entities = [result[0][1] for result in results]

    return JSONResponse(matched_entities)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


app.include_router(registration.router, prefix="/register")
app.include_router(login.router, prefix="/login")
app.include_router(event.router, prefix="/event")
