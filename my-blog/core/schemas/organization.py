from pydantic import BaseModel
import uuid

class OrganizationSchema(BaseModel):
    id: uuid.UUID
    name: str
    tenant_id: str

    class Config:
        orm_mode = True
