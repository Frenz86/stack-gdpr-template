from pydantic import BaseModel, EmailStr
import uuid

class UserSchema(BaseModel):
    id: uuid.UUID
    email: EmailStr
    name: str

    class Config:
        orm_mode = True
