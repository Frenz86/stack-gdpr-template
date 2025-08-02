from pydantic import BaseModel, UUID4, datetime

class DataSubjectRequestSchema(BaseModel):
    user_id: UUID4
    request_type: str
    status: str
    timestamp: datetime
