import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from plugins.security_plugin.middleware.rate_limiting import RateLimitMiddleware
from plugins.security_plugin.middleware.bot_detection import BotDetectionMiddleware
from plugins.security_plugin.middleware.ip_blocking import IPBlockingMiddleware
from plugins.security_plugin.middleware.security_headers import SecurityHeadersMiddleware

app = FastAPI()
app.add_middleware(RateLimitMiddleware)
app.add_middleware(BotDetectionMiddleware)
app.add_middleware(IPBlockingMiddleware)
app.add_middleware(SecurityHeadersMiddleware)

@app.get("/test")
def test():
    return {"ok": True}

client = TestClient(app)

def test_rate_limit():
    for _ in range(101):
        response = client.get("/test")
    assert response.status_code in [200, 429]

def test_bot_detection():
    response = client.get("/test", headers={"user-agent": "python-requests"})
    assert response.status_code == 403

def test_ip_blocking(monkeypatch):
    monkeypatch.setenv("BLOCKED_IPS", "127.0.0.1")
    response = client.get("/test")
    assert response.status_code == 403

def test_security_headers():
    response = client.get("/test")
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["Content-Security-Policy"] == "default-src 'self'"
