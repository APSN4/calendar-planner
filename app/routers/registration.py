from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.database.db import get_db
from app.models.user import User, UserCreate
from app.service.register import register

router = APIRouter()
templates = Jinja2Templates(directory="app/frontend")

@router.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse(
        request=request, name="registration.html"
    )

@router.post("/")
async def register_user(name: str = Form(...), surname: str = Form(...), email: str = Form(...), password: str = Form(...)):
    user = UserCreate(name=name, surname=surname, email=email, password=password)
    register(next(get_db()), user)  # next(), чтобы получить объект сессии базы данных из генератора
    return {"message": "User registered successfully!"}