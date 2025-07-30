import pytest
from fastapi.testclient import TestClient
from plugins.analytics_plugin.api import router
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

# Setup test app
from fastapi import FastAPI
app = FastAPI()
app.include_router(router)

# Setup test DB
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

def test_track_event():
    response = client.post("/analytics/event", json={"event_type": "login", "user_id": 1, "data": "{'ip':'127.0.0.1'}"})
    assert response.status_code == 200
    assert response.json()["event_type"] == "login"

def test_stats():
    client.post("/analytics/event", json={"event_type": "view", "user_id": 2, "data": "{'page':'home'}"})
    response = client.get("/analytics/stats")
    assert response.status_code == 200
    assert "total_events" in response.json()

def test_analytics_health():
    response = client.get("/analytics/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "plugin": "analytics"}
