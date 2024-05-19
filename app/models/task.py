from pydantic import BaseModel


class Task(BaseModel):
    id: int
    description: str
    completed: bool = False

    class Config:
        orm_mode = True


class TaskCreate(BaseModel):
    description: str
