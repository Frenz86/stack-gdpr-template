from pydantic import BaseModel, UUID4, datetime

class AuditLogSchema(BaseModel):
    event_type: str
    user_id: UUID4 | None = None
    details: str | None = None
    timestamp: datetime

class SecurityLogSchema(BaseModel):
    event_type: str
    user_id: UUID4 | None = None
    details: str | None = None
    timestamp: datetime
