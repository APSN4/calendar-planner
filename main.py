from fastapi import FastAPI
from app.routers import items, users

"""

Запуск производится командой: fastapi run
Переход осуществляется по локальному IP в сети. [win cmd: ipconfig]

"""

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

app.include_router(items.router, prefix="/api/items")
app.include_router(users.router, prefix="/api/users")
