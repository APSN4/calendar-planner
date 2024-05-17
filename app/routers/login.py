from fastapi import APIRouter, Request, Form, Response, Depends, Cookie, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.database.db import get_db
from app.models.user import User, UserCreate, UserLogin
from app.service.login import login_service
from fastapi.responses import RedirectResponse

from app.service.md5 import calculate_md5

router = APIRouter()
templates = Jinja2Templates(directory="app/frontend")


@router.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse(
        request=request, name="login.html"
    )


@router.post("/")
async def login_user(response: Response, email: str = Form(...), password: str = Form(...)):
    user = UserLogin(email=email, password=password)
    user_bd = login_service(next(get_db()), user)
    if user_bd is not None and user_bd.password == password:
        response_redirect = RedirectResponse(url="/", status_code=303)
        response_redirect.set_cookie(key="token", value=calculate_md5(f"{email}:{password}"))
        return response_redirect
    else:
        response_redirect = RedirectResponse(url="/login/?error=auth", status_code=303)
        return response_redirect
