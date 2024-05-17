import logging

from fastapi import FastAPI, Request, Cookie, Depends, Response

from app.database.db import Base, engine
from app.routers import items, users, registration, login

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

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
async def read_item(request: Request, token: str = Depends(verify_token)):
    try:
        cookie = token.title()
    except Exception as e:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse(
        request=request, name="index.html"
    )

@app.post("/exit")
async def exit_user():
    response_redirect = RedirectResponse(url="/login", status_code=303)
    response_redirect.delete_cookie(key="token")
    return response_redirect

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


app.include_router(items.router, prefix="/api/items")
app.include_router(users.router, prefix="/api/users")
app.include_router(registration.router, prefix="/register")
app.include_router(login.router, prefix="/login")
