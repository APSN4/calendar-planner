from pydantic import BaseModel


class Task(BaseModel):
    description: list[dict] = []
    completed: bool = False

    class Config:
        orm_mode = True


class TaskCreate(BaseModel):
    description: str
