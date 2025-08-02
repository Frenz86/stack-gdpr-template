from .models import AnalyticsEvent
from .schemas import AnalyticsEventOut

def log_event(db, event_type, user_id=None, data=""):
    event = AnalyticsEvent(event_type=event_type, user_id=user_id, data=data)
    db.add(event)
    db.commit()
    db.refresh(event)
    return AnalyticsEventOut.from_orm(event)

def get_stats(db):
    total = db.query(AnalyticsEvent).count()
    by_type = db.query(AnalyticsEvent.event_type, db.func.count(AnalyticsEvent.id)).group_by(AnalyticsEvent.event_type).all()
    return {"total_events": total, "events_by_type": dict(by_type)}
