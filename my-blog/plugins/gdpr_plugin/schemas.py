from pydantic import BaseModel
from typing import Optional
import datetime

class ConsentCreate(BaseModel):
    user_id: int
    type: str
    accepted: bool

class ConsentOut(BaseModel):
    id: int
    user_id: int
    type: str
    accepted: bool
    accepted_at: datetime.datetime
    revoked_at: Optional[datetime.datetime]

    class Config:
        orm_mode = True

class PolicyVersionOut(BaseModel):
    id: int
    policy_type: str
    version: str
    published_at: datetime.datetime
    url: str

    class Config:
        orm_mode = True

class AdminActionLogOut(BaseModel):
    id: int
    admin_id: int
    action: str
    target_user_id: int | None
    details: str
    created_at: datetime.datetime

    class Config:
        orm_mode = True
