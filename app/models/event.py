from pydantic import BaseModel


class Event(BaseModel):
    date: str
    time: str
    place: str
    budget: str
    description: str
    task_list: list = []
    progress_bar: int  # [0-100]
    alert: list[int] = []
    status: int  # 0, 1, 2
