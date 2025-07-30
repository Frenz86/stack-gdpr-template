from fastapi import APIRouter

router = APIRouter()

@router.get("/analytics/health", tags=["Analytics"], summary="Analytics plugin health check")
def analytics_health():
    return {"status": "ok", "plugin": "analytics"}
