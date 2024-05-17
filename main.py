from fastapi import FastAPI, Request

from app.database.db import Base, engine
from app.routers import items, users, registration

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

"""

Запуск производится командой: fastapi run
Переход осуществляется по локальному IP в сети. [win cmd: ipconfig]

"""

app = FastAPI()
templates = Jinja2Templates(directory="app/frontend")


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


app.include_router(items.router, prefix="/api/items")
app.include_router(users.router, prefix="/api/users")
app.include_router(registration.router, prefix="/register")
