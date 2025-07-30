"""
Test automatici per gli endpoint di legal compliance GDPR
"""
import pytest
from fastapi.testclient import TestClient
from core.main import app

client = TestClient(app)

def test_create_dpia():
    response = client.post("/api/gdpr/legal/dpia/create", json={
        "project_name": "Test Project",
        "processing_description": "Test processing",
        "necessity_justification": "Required for test",
        "risks": ["risk1", "risk2"],
        "mitigations": ["mit1", "mit2"]
    })
    assert response.status_code == 200
    assert "dpia_id" in response.json()

def test_get_legal_basis_not_found():
    response = client.get("/api/gdpr/legal/legal-basis/nonexistent")
    assert response.status_code == 404

def test_minor_consent_verify_not_found():
    response = client.post("/api/gdpr/legal/minor-consent/verify", json={
        "user_id": "00000000-0000-0000-0000-000000000000",
        "parent_token": "invalidtoken"
    })
    assert response.status_code == 404

def test_generate_compliance_report():
    response = client.get("/api/gdpr/legal/compliance-report/monthly")
    assert response.status_code == 200
    assert "report_id" in response.json()
    assert "metrics" in response.json()
