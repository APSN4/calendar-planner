from pydantic import BaseModel


class Task(BaseModel):
    description: list[dict] = []
    completed: bool = False
