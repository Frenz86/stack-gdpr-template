from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid
import datetime

Base = declarative_base()

class DataSubjectRequest(Base):
    __tablename__ = "gdpr_data_subject_requests"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    request_type = Column(String, nullable=False)  # e.g. 'access', 'erasure', 'portability'
    status = Column(String, default="pending")
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
