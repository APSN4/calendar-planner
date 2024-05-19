from pydantic import BaseModel


class Event(BaseModel):
    date: str
    time: str
    place: str
    budget: int
    description: str
    task_list: list = []
    progress_bar: int  # [0-100]
    alert: str
    files: list[str] = []

    class Config:
        orm_mode = True


class EventCreate(BaseModel):
    date: str
    time: str
    place: str
    budget: int
    description: str
    alert: str


class EventUpdatePost(BaseModel):
    event_id: int
    date: str
    time: str
    place: str
    budget: int
    description: str
    alert: str


class EventDelete(BaseModel):
    id: int


class EventGet(BaseModel):
    id: int


class EventUpdate(BaseModel):
    task_list: list = []


class UploadFileEvent(BaseModel):
    event_id: int
    files: list = []


class GetFileEvent(BaseModel):
    event_id: int
    file_id: int
