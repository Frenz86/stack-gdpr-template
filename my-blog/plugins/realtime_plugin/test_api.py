import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from plugins.realtime_plugin.api import router

app = FastAPI()
app.include_router(router)
client = TestClient(app)

def test_sse_dashboard():
    response = client.get("/sse/dashboard", headers={"accept": "text/event-stream"})
    assert response.status_code == 200
    assert "data: update" in response.text

def test_websocket_notifications():
    with client.websocket_connect("/ws/notifications") as websocket:
        websocket.send_text("test")
        data = websocket.receive_text()
        assert "Notifica ricevuta: test" in data
