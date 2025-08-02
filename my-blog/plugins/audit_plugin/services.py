from .models import AuditLog
from .schemas import AuditLogOut

def log_audit(db, user_id=None, action="", details=""):
    log = AuditLog(user_id=user_id, action=action, details=details)
    db.add(log)
    db.commit()
    db.refresh(log)
    return AuditLogOut.from_orm(log)

def get_audit_logs(db):
    logs = db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(100).all()
    return [AuditLogOut.from_orm(l) for l in logs]
