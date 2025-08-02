from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .models import Consent, PolicyVersion
from .schemas import ConsentCreate, ConsentOut, PolicyVersionOut, AdminActionLogOut

router = APIRouter(prefix="/gdpr", tags=["GDPR"])

@router.post("/consent", response_model=ConsentOut)
def set_consent(consent: ConsentCreate, db: Session = Depends()):
    db_consent = Consent(user_id=consent.user_id, type=consent.type, accepted=consent.accepted)
    db.add(db_consent)
    db.commit()
    db.refresh(db_consent)
    return db_consent

@router.post("/consent/revoke", response_model=ConsentOut)
def revoke_consent(user_id: int, type: str, db: Session = Depends()):
    db_consent = db.query(Consent).filter_by(user_id=user_id, type=type, accepted=True).first()
    if db_consent:
        db_consent.accepted = False
        db_consent.revoked_at = db_consent.revoked_at or db_consent.accepted_at
        db.commit()
        db.refresh(db_consent)
    return db_consent

@router.get("/consent", response_model=list[ConsentOut])
def list_consents(user_id: int, db: Session = Depends()):
    return db.query(Consent).filter_by(user_id=user_id).all()

@router.get("/policy/version", response_model=list[PolicyVersionOut])
def get_policy_versions(policy_type: str = None, db: Session = Depends()):
    q = db.query(PolicyVersion)
    if policy_type:
        q = q.filter_by(policy_type=policy_type)
    return q.order_by(PolicyVersion.published_at.desc()).all()

@router.post("/admin/log", response_model=AdminActionLogOut)
def log_admin_action(admin_id: int, action: str, target_user_id: int = None, details: str = "", db: Session = Depends()):
    from .models import AdminActionLog
    log = AdminActionLog(admin_id=admin_id, action=action, target_user_id=target_user_id, details=details)
    db.add(log)
    db.commit()
    db.refresh(log)
    return log

@router.get("/admin/logs", response_model=list[AdminActionLogOut])
def list_admin_logs(admin_id: int = None, db: Session = Depends()):
    from .models import AdminActionLog
    q = db.query(AdminActionLog)
    if admin_id:
        q = q.filter_by(admin_id=admin_id)
    return q.order_by(AdminActionLog.created_at.desc()).limit(100).all()

@router.get("/metrics")
def get_gdpr_metrics(db: Session = Depends()):
    from .models import Consent, PolicyVersion, AdminActionLog
    # Consensi
    consents_active = db.query(Consent).filter_by(accepted=True).count()
    consents_expired = db.query(Consent).filter_by(accepted=False).count()
    # Export Dati
    exports_requested = db.execute("SELECT COUNT(*) FROM export_requests").scalar() if db.bind.has_table("export_requests") else 0
    exports_completed = db.execute("SELECT COUNT(*) FROM export_requests WHERE status='completed'").scalar() if db.bind.has_table("export_requests") else 0
    # Cancellazioni
    deletions_requested = db.execute("SELECT COUNT(*) FROM deletion_requests").scalar() if db.bind.has_table("deletion_requests") else 0
    deletions_completed = db.execute("SELECT COUNT(*) FROM deletion_requests WHERE status='completed'").scalar() if db.bind.has_table("deletion_requests") else 0
    # Data Breach
    breach_notified = db.execute("SELECT COUNT(*) FROM breach_notifications").scalar() if db.bind.has_table("breach_notifications") else 0
    # Policy Versioning
    policy_versions = [
        {"version": v.version, "date": v.published_at.strftime("%Y-%m-%d")}
        for v in db.query(PolicyVersion).order_by(PolicyVersion.published_at.desc()).all()
    ]
    # Audit Trail
    audit_logs_count = db.query(AdminActionLog).count()
    # DPO Requests
    dpo_requests = db.execute("SELECT COUNT(*) FROM dpo_requests").scalar() if db.bind.has_table("dpo_requests") else 0
    dpo_resolved = db.execute("SELECT COUNT(*) FROM dpo_requests WHERE status='resolved'").scalar() if db.bind.has_table("dpo_requests") else 0
    return {
        "consents_active": consents_active,
        "consents_expired": consents_expired,
        "exports_requested": exports_requested,
        "exports_completed": exports_completed,
        "deletions_requested": deletions_requested,
        "deletions_completed": deletions_completed,
        "breach_notified": breach_notified,
        "policy_versions": policy_versions,
        "audit_logs_count": audit_logs_count,
        "dpo_requests": dpo_requests,
        "dpo_resolved": dpo_resolved
    }
