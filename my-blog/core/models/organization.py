from sqlalchemy import Column, String
from core.models.base import BaseModel

class Organization(BaseModel):
    __tablename__ = "organizations"
    name = Column(String, nullable=False)
    tenant_id = Column(String, unique=True, nullable=False)
