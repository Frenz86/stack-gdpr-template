from pydantic import BaseModel
from typing import Optional

class AuditLogCreate(BaseModel):
    user_id: Optional[int] = None
    action: str
    details: str = ""

class AuditLogOut(BaseModel):
    id: int
    user_id: Optional[int]
    action: str
    details: str
    created_at: str

    class Config:
        orm_mode = True
