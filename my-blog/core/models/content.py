from sqlalchemy import Column, String, Text
from core.models.base import BaseModel

class Content(BaseModel):
    __tablename__ = "contents"
    title = Column(String, nullable=False)
    body = Column(Text, nullable=False)
