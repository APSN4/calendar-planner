from pydantic import BaseModel


class File(BaseModel):
    id: int
    content: bytes
    filename: str

    class Config:
        orm_mode = True


class FileUpload(BaseModel):
    content: bytes
    filename: str
