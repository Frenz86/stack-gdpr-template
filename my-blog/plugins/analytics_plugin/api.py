from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .models import AnalyticsEvent
from .schemas import AnalyticsEventCreate, AnalyticsEventOut
from plugins.analytics_plugin.services import log_event, get_stats

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.post("/event", response_model=AnalyticsEventOut)
def track_event(event: AnalyticsEventCreate, db: Session = Depends()):
    return log_event(db, event.event_type, event.user_id, event.data)

@router.get("/stats")
def stats(db: Session = Depends()):
    return get_stats(db)
