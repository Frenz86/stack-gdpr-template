# plugins/gdpr_plugin/api/gdpr_endpoints.py
"""
Missing GDPR API endpoints for demo functionality
Add these to your plugins/gdpr_plugin/api.py file
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
import json
from datetime import datetime, timedelta
from core.dependencies import get_db

router = APIRouter(prefix="/api/gdpr", tags=["GDPR"])

# Mock data for demo - replace with real DB queries
DEMO_DATA = {
    "users": [
        {"id": 1, "email": "user1@demo.com", "name": "Demo User 1", "created_at": "2024-01-01"},
        {"id": 2, "email": "user2@demo.com", "name": "Demo User 2", "created_at": "2024-01-15"},
        {"id": 3, "email": "user3@demo.com", "name": "Demo User 3", "created_at": "2024-02-01"},
    ],
    "consents": [
        {"id": 1, "user_id": 1, "type": "marketing", "accepted": True, "created_at": "2024-01-01"},
        {"id": 2, "user_id": 1, "type": "analytics", "accepted": True, "created_at": "2024-01-01"},
        {"id": 3, "user_id": 2, "type": "marketing", "accepted": False, "created_at": "2024-01-15"},
        {"id": 4, "user_id": 3, "type": "analytics", "accepted": True, "created_at": "2024-02-01"},
    ],
    "exports": [
        {"id": 1, "user_id": 1, "status": "completed", "requested_at": "2024-01-05"},
        {"id": 2, "user_id": 2, "status": "pending", "requested_at": "2024-01-20"},
    ],
    "deletions": [
        {"id": 1, "user_id": 3, "status": "completed", "requested_at": "2024-02-05", "reason": "GDPR request"},
    ],
    "audit_logs": [
        {"id": 1, "user_id": 1, "action": "consent_given", "details": "Marketing consent", "timestamp": "2024-01-01T10:00:00"},
        {"id": 2, "user_id": 1, "action": "data_export", "details": "Full data export", "timestamp": "2024-01-05T14:30:00"},
        {"id": 3, "user_id": 2, "action": "consent_revoked", "details": "Marketing consent revoked", "timestamp": "2024-01-15T09:15:00"},
        {"id": 4, "user_id": 3, "action": "account_deletion", "details": "Full account deletion", "timestamp": "2024-02-05T16:45:00"},
    ]
}

@router.get("/metrics")
async def get_gdpr_metrics():
    """Real-time GDPR compliance metrics for dashboard"""
    
    # Calculate metrics from demo data
    active_consents = len([c for c in DEMO_DATA["consents"] if c["accepted"]])
    expired_consents = len([c for c in DEMO_DATA["consents"] if not c["accepted"]])
    
    exports_requested = len(DEMO_DATA["exports"])
    exports_completed = len([e for e in DEMO_DATA["exports"] if e["status"] == "completed"])
    
    deletions_requested = len(DEMO_DATA["deletions"])
    deletions_completed = len([d for d in DEMO_DATA["deletions"] if d["status"] == "completed"])
    
    total_users = len(DEMO_DATA["users"])
    audit_logs_count = len(DEMO_DATA["audit_logs"])
    
    # Calculate compliance score
    compliance_factors = {
        "consent_coverage": min(100, (active_consents / max(total_users, 1)) * 100),
        "data_requests_handled": min(100, (exports_completed / max(exports_requested, 1)) * 100) if exports_requested > 0 else 100,
        "deletions_handled": min(100, (deletions_completed / max(deletions_requested, 1)) * 100) if deletions_requested > 0 else 100,
        "audit_completeness": min(100, (audit_logs_count / max(total_users * 2, 1)) * 100),
    }
    
    compliance_score = int(sum(compliance_factors.values()) / len(compliance_factors))
    
    return {
        "compliance_score": compliance_score,
        "consents_active": active_consents,
        "consents_expired": expired_consents,
        "exports_requested": exports_requested,
        "exports_completed": exports_completed,
        "deletions_requested": deletions_requested,
        "deletions_completed": deletions_completed,
        "breach_notified": 0,  # Demo: no breaches
        "audit_logs_count": audit_logs_count,
        "dpo_requests": 0,  # Demo: no DPO requests
        "dpo_resolved": 0,
        "total_users": total_users,
        "compliance_factors": compliance_factors,
        "last_updated": datetime.now().isoformat()
    }

@router.get("/export")
async def export_user_data(user_id: int, format: str = "json"):
    """Export all user data (GDPR Article 20 - Right to Data Portability)"""
    
    # Find user
    user = next((u for u in DEMO_DATA["users"] if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Collect all user data
    user_consents = [c for c in DEMO_DATA["consents"] if c["user_id"] == user_id]
    user_exports = [e for e in DEMO_DATA["exports"] if e["user_id"] == user_id]
    user_audit = [a for a in DEMO_DATA["audit_logs"] if a["user_id"] == user_id]
    
    export_data = {
        "user_profile": user,
        "consents": user_consents,
        "export_history": user_exports,
        "audit_trail": user_audit,
        "exported_at": datetime.now().isoformat(),
        "export_format": format,
        "gdpr_notice": "This export contains all personal data we have about you as per GDPR Article 20."
    }
    
    # Log the export
    DEMO_DATA["audit_logs"].append({
        "id": len(DEMO_DATA["audit_logs"]) + 1,
        "user_id": user_id,
        "action": "data_export",
        "details": f"Data exported in {format} format",
        "timestamp": datetime.now().isoformat()
    })
    
    # Add to exports tracking
    DEMO_DATA["exports"].append({
        "id": len(DEMO_DATA["exports"]) + 1,
        "user_id": user_id,
        "status": "completed",
        "requested_at": datetime.now().isoformat()
    })
    
    return export_data

@router.delete("/delete-account")
async def delete_user_account(user_id: int, reason: str = "User request"):
    """Delete user account (GDPR Article 17 - Right to Erasure)"""
    
    # Find user
    user = next((u for u in DEMO_DATA["users"] if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Log deletion before removing data
    DEMO_DATA["audit_logs"].append({
        "id": len(DEMO_DATA["audit_logs"]) + 1,
        "user_id": user_id,
        "action": "account_deletion",
        "details": f"Account deleted. Reason: {reason}",
        "timestamp": datetime.now().isoformat()
    })
    
    # Add to deletions tracking
    DEMO_DATA["deletions"].append({
        "id": len(DEMO_DATA["deletions"]) + 1,
        "user_id": user_id,
        "status": "completed",
        "requested_at": datetime.now().isoformat(),
        "reason": reason
    })
    
    # Simulate data anonymization (in real app, you'd anonymize rather than delete for audit purposes)
    user["email"] = f"deleted_user_{user_id}@anonymized.local"
    user["name"] = f"Anonymized User {user_id}"
    user["deleted_at"] = datetime.now().isoformat()
    
    return {
        "status": "deleted",
        "user_id": user_id,
        "message": "User account has been deleted and data anonymized",
        "deleted_at": datetime.now().isoformat(),
        "audit_trail": "Deletion logged in audit trail"
    }

@router.post("/consent")
async def create_consent(user_id: int, consent_type: str, accepted: bool):
    """Create or update user consent (GDPR Article 7 - Consent)"""
    
    # Check if consent already exists
    existing_consent = next((c for c in DEMO_DATA["consents"] if c["user_id"] == user_id and c["type"] == consent_type), None)
    
    if existing_consent:
        existing_consent["accepted"] = accepted
        existing_consent["updated_at"] = datetime.now().isoformat()
        consent_id = existing_consent["id"]
        action = "consent_updated"
    else:
        consent_id = len(DEMO_DATA["consents"]) + 1
        new_consent = {
            "id": consent_id,
            "user_id": user_id,
            "type": consent_type,
            "accepted": accepted,
            "created_at": datetime.now().isoformat()
        }
        DEMO_DATA["consents"].append(new_consent)
        action = "consent_given" if accepted else "consent_denied"
    
    # Log the consent action
    DEMO_DATA["audit_logs"].append({
        "id": len(DEMO_DATA["audit_logs"]) + 1,
        "user_id": user_id,
        "action": action,
        "details": f"{consent_type} consent {'granted' if accepted else 'denied'}",
        "timestamp": datetime.now().isoformat()
    })
    
    return {
        "status": "success",
        "consent_id": consent_id,
        "user_id": user_id,
        "type": consent_type,
        "accepted": accepted,
        "message": f"Consent for {consent_type} has been {'granted' if accepted else 'denied'}"
    }

@router.post("/consent/revoke")
async def revoke_consent(user_id: int, consent_type: str):
    """Revoke user consent (GDPR Article 7 - Withdrawal of consent)"""
    
    # Find and revoke consent
    consent = next((c for c in DEMO_DATA["consents"] if c["user_id"] == user_id and c["type"] == consent_type), None)
    if not consent:
        raise HTTPException(status_code=404, detail="Consent not found")
    
    consent["accepted"] = False
    consent["revoked_at"] = datetime.now().isoformat()
    
    # Log revocation
    DEMO_DATA["audit_logs"].append({
        "id": len(DEMO_DATA["audit_logs"]) + 1,
        "user_id": user_id,
        "action": "consent_revoked",
        "details": f"{consent_type} consent revoked",
        "timestamp": datetime.now().isoformat()
    })
    
    return {
        "status": "revoked",
        "consent_id": consent["id"],
        "user_id": user_id,
        "type": consent_type,
        "revoked_at": consent["revoked_at"],
        "message": f"Consent for {consent_type} has been revoked"
    }

@router.get("/consent")
async def list_user_consents(user_id: int):
    """List all consents for a user"""
    user_consents = [c for c in DEMO_DATA["consents"] if c["user_id"] == user_id]
    return {
        "user_id": user_id,
        "consents": user_consents,
        "total_consents": len(user_consents),
        "active_consents": len([c for c in user_consents if c["accepted"]])
    }

@router.post("/breach")
async def report_data_breach(description: str, affected_users: Optional[int] = 0):
    """Report data breach (GDPR Article 33 - Notification of breach)"""
    
    breach_id = "BREACH_" + datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Log breach
    DEMO_DATA["audit_logs"].append({
        "id": len(DEMO_DATA["audit_logs"]) + 1,
        "user_id": None,
        "action": "data_breach_reported",
        "details": f"Breach ID: {breach_id}. Description: {description}. Affected users: {affected_users}",
        "timestamp": datetime.now().isoformat()
    })
    
    return {
        "status": "reported",
        "breach_id": breach_id,
        "reported_at": datetime.now().isoformat(),
        "description": description,
        "affected_users": affected_users,
        "notified": True,
        "message": "Data breach has been reported and logged",
        "next_steps": [
            "Supervisory authority will be notified within 72 hours",
            "Affected users will be notified if high risk",
            "Breach assessment and mitigation in progress"
        ]
    }

@router.get("/audit-logs")
async def get_audit_logs(user_id: Optional[int] = None, limit: int = 50):
    """Get audit logs for GDPR operations"""
    
    logs = DEMO_DATA["audit_logs"]
    
    if user_id:
        logs = [log for log in logs if log["user_id"] == user_id]
    
    # Sort by timestamp (newest first) and limit
    logs = sorted(logs, key=lambda x: x["timestamp"], reverse=True)[:limit]
    
    return {
        "audit_logs": logs,
        "total_logs": len(DEMO_DATA["audit_logs"]),
        "filtered_logs": len(logs),
        "user_filter": user_id
    }

# Operational Excellence endpoints for dashboard
@router.get("/ops/dashboard/metrics")
async def get_dashboard_metrics():
    """Real-time dashboard metrics with additional operational data"""
    
    base_metrics = await get_gdpr_metrics()
    
    # Additional operational metrics
    recent_audits = [
        f"{log['action']} - User {log['user_id']} - {log['timestamp'][:10]}"
        for log in sorted(DEMO_DATA["audit_logs"], key=lambda x: x["timestamp"], reverse=True)[:5]
    ]
    
    security_alerts = [
        "Rate limiting active - 100 req/min limit",
        "Bot detection enabled",
        "Security headers configured"
    ]
    
    return {
        **base_metrics,
        "active_consents": base_metrics["consents_active"],
        "pending_requests": base_metrics["exports_requested"] - base_metrics["exports_completed"],
        "recent_audits": recent_audits,
        "security_alerts": security_alerts,
        "data_retention_status": "Compliant - 30 day retention policy active",
        "system_status": "Operational",
        "last_backup": (datetime.now() - timedelta(hours=6)).isoformat(),
        "next_compliance_check": (datetime.now() + timedelta(hours=18)).isoformat()
    }

# Test endpoint for demo
@router.get("/test")
async def test_endpoint():
    """Test endpoint for security middleware testing"""
    return {
        "status": "ok",
        "message": "Test endpoint for security and rate limiting demo",
        "timestamp": datetime.now().isoformat()
    }