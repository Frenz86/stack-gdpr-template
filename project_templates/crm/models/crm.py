# Modello base CRM

from pydantic import BaseModel
from datetime import datetime

class Customer(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime
    active: bool = True

class Interaction(BaseModel):
    id: int
    customer_id: int
    type: str
    note: str
    date: datetime
