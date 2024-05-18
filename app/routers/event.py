import json

from fastapi import APIRouter, Request, Form, Depends, Cookie
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.database.db import get_db
from app.models.event import EventCreate, EventDelete
from app.models.user import User, UserCreate, UserId
from app.service.crud import delete_event
from app.service.event import create_event_db, get_user_by_id, update_user_db, parse_pg_array
from app.service.md5 import calculate_md5
from app.service.register import register
from fastapi.responses import RedirectResponse

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
async def event_create(user_id: str = Depends(verify_user_id), date: str = Form(...), time: str = Form(...), place: str = Form(...), budget: str = Form(...), description: str = Form(...),
                       reminder_time: str = Form(...)):
    event = EventCreate(date=date, time=time, place=place, budget=budget, description=description, alert=reminder_time)
    new_event = create_event_db(next(get_db()), event)
    try:
        user_id = user_id.title()
    except Exception as e:
        return RedirectResponse(url="/")
    user = UserId(id=user_id)
    user_bd = get_user_by_id(next(get_db()), user)
    event_list = json.loads(str(parse_pg_array(user_bd.event_list)))
    event_list.append(new_event.id)
    user_bd.event_list = event_list
    update_user_db(next(get_db()), int(user_id), user_bd)

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
