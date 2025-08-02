from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid
import datetime

Base = declarative_base()

class DataRetentionPolicy(Base):
    __tablename__ = "gdpr_data_retention_policies"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    policy_name = Column(String, nullable=False)
    retention_days = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
