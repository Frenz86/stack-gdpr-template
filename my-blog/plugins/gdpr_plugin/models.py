from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
import datetime
from core.database.base import Base, BaseModel, PluginRegistry

class Consent(BaseModel):
    __tablename__ = "consents"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    type = Column(String, index=True)  # es: marketing, analytics, profiling
    accepted = Column(Boolean, default=False)
    accepted_at = Column(DateTime, default=datetime.datetime.utcnow)
    revoked_at = Column(DateTime, nullable=True)

class PolicyVersion(BaseModel):
    __tablename__ = "policy_versions"
    id = Column(Integer, primary_key=True, index=True)
    policy_type = Column(String, index=True)  # privacy, cookie
    version = Column(String)
    published_at = Column(DateTime, default=datetime.datetime.utcnow)
    url = Column(String)

class AdminActionLog(BaseModel):
    __tablename__ = "admin_action_logs"
    id = Column(Integer, primary_key=True, index=True)
    admin_id = Column(Integer, index=True)
    action = Column(String)
    target_user_id = Column(Integer, index=True, nullable=True)
    details = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
