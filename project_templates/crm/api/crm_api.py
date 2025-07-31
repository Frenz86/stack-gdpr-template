# API base CRM

from fastapi import APIRouter
from project_templates.crm.models.crm import Customer, Interaction
from datetime import datetime

router = APIRouter()

@router.get("/customers", response_model=list[Customer])
def list_customers():
    # Dummy data
    return [Customer(id=1, name="Mario Rossi", email="mario@azienda.it", created_at=datetime.now())]

@router.get("/interactions", response_model=list[Interaction])
def list_interactions():
    # Dummy data
    return [Interaction(id=1, customer_id=1, type="email", note="Richiesta informazioni", date=datetime.now())]
