from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .models import AuditLog
from .schemas import AuditLogCreate, AuditLogOut
from plugins.audit_plugin.services import log_audit, get_audit_logs

router = APIRouter(prefix="/audit", tags=["Audit"])

@router.post("/log", response_model=AuditLogOut)
def audit_log(log: AuditLogCreate, db: Session = Depends()):
    return log_audit(db, log.user_id, log.action, log.details)

@router.get("/logs", response_model=list[AuditLogOut])
def logs(db: Session = Depends()):
    return get_audit_logs(db)
