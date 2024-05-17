from pydantic import BaseModel, EmailStr


class User(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: str
    event_list: list = []

    class Config:
        orm_mode = True



