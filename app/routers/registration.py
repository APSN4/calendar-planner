from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.database.db import get_db
from app.models.user import User, UserCreate
from app.service.md5 import calculate_md5
from app.service.register import register
from fastapi.responses import RedirectResponse

router = APIRouter()
templates = Jinja2Templates(directory="app/frontend")


@router.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse(
        request=request, name="registration.html"
    )


@router.post("/")
async def register_user(name: str = Form(...), surname: str = Form(...), email: str = Form(...),
                        password: str = Form(...)):
    user = UserCreate(name=name, surname=surname, email=email, password=password)
    user_bd = register(next(get_db()), user)  # next(), чтобы получить объект сессии базы данных из генератора
    response_redirect = RedirectResponse(url="/", status_code=303)
    response_redirect.set_cookie(key="token", value=calculate_md5(f"{email}:{password}"))
    response_redirect.set_cookie(key="user_id", value=user_bd.id)
    return response_redirect
