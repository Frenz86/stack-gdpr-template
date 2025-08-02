from fastapi import APIRouter

router = APIRouter()

@router.get("/audit/health", tags=["Audit"], summary="Audit plugin health check")
def audit_health():
    return {"status": "ok", "plugin": "audit"}
