from sqlalchemy import Column, Integer, String, DateTime, Text
import datetime
from core.database.base import Base, BaseModel, PluginRegistry

class AnalyticsEvent(BaseModel):
    __tablename__ = "analytics_events"
    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String, index=True)
    user_id = Column(Integer, index=True, nullable=True)
    data = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
