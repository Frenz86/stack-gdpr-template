from pydantic import BaseModel
import uuid

class ContentSchema(BaseModel):
    id: uuid.UUID
    title: str
    body: str

    class Config:
        orm_mode = True
