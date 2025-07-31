# Service base CRM

from project_templates.crm.models.crm import Customer, Interaction
from datetime import datetime

def get_all_customers():
    return [Customer(id=1, name="Mario Rossi", email="mario@azienda.it", created_at=datetime.now())]

def get_all_interactions():
    return [Interaction(id=1, customer_id=1, type="email", note="Richiesta informazioni", date=datetime.now())]
