from sqlalchemy import Column, Integer, String, DateTime, Text
from core.database.base import Base, BaseModel, PluginRegistry
import datetime


class AuditLog(BaseModel):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=True)
    action = Column(String)
    details = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
