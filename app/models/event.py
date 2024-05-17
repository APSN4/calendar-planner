from pydantic import BaseModel


class Event(BaseModel):
    date: str
    time: str
    place: str
    budget: int
    description: str
    task_list: list = []
    progress_bar: int  # [0-100]
    alert: int
    status: int  # 0, 1, 2

    class Config:
        orm_mode = True


class EventCreate(BaseModel):
    date: str
    time: str
    place: str
    budget: int
    description: str

