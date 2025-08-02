from pydantic import BaseModel, UUID4, datetime

class ConsentPreferences(BaseModel):
    user_id: UUID4
    consent_type: str
    given: bool
    timestamp: datetime
    expiry: datetime | None = None

class ConsentWithdrawalSchema(BaseModel):
    user_id: UUID4
    consent_type: str
    timestamp: datetime
