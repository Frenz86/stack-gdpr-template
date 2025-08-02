from pydantic import BaseModel
from typing import Optional

class AnalyticsEventCreate(BaseModel):
    event_type: str
    user_id: Optional[int] = None
    data: str = ""

class AnalyticsEventOut(BaseModel):
    id: int
    event_type: str
    user_id: Optional[int]
    data: str
    created_at: str

    class Config:
        orm_mode = True
