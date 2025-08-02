from sqlalchemy import Column, String
from core.models.base import BaseModel

class User(BaseModel):
    __tablename__ = "users"
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
