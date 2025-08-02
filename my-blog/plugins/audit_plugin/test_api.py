import pytest
from fastapi.testclient import TestClient
from plugins.audit_plugin.api import router
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

from fastapi import FastAPI
app = FastAPI()
app.include_router(router)

engine = create_engine("sqlite:///:memory:")
TestingSessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides = { }
client = TestClient(app)

def test_audit_log():
    response = client.post("/audit/log", json={"user_id": 1, "action": "delete", "details": "Deleted record"})
    assert response.status_code == 200
    assert response.json()["action"] == "delete"

def test_logs():
    client.post("/audit/log", json={"user_id": 2, "action": "update", "details": "Updated record"})
    response = client.get("/audit/logs")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
