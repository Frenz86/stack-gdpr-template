import pytest
from fastapi.testclient import TestClient
from plugins.gdpr_plugin.api import router
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

def test_log_admin_action():
    response = client.post("/gdpr/admin/log", json={"admin_id": 1, "action": "delete", "target_user_id": 2, "details": "Deleted user"})
    assert response.status_code == 200
    assert response.json()["action"] == "delete"

def test_list_admin_logs():
    client.post("/gdpr/admin/log", json={"admin_id": 2, "action": "update", "target_user_id": 3, "details": "Updated user"})
    response = client.get("/gdpr/admin/logs")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1
