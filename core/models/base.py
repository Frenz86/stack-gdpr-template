from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid
import datetime

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    tenant_id = Column(UUID(as_uuid=True), nullable=False, index=True)

    @classmethod
    def for_tenant(cls, session, tenant_id):
        return session.query(cls).filter_by(tenant_id=tenant_id)
