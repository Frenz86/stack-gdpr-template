# Modello base Blog

from pydantic import BaseModel
from datetime import datetime

class BlogPost(BaseModel):
    id: int
    title: str
    content: str
    author: str
    created_at: datetime
    tags: list[str] = []
    published: bool = True

class BlogComment(BaseModel):
    id: int
    post_id: int
    author: str
    content: str
    created_at: datetime
