"""
Celery application instance for stack-gdpr-template
"""
import os
from celery import Celery
from core.config import settings

celery_app = Celery(
    "stack_gdpr_template",
    broker=settings.CELERY_BROKER_URL or settings.REDIS_URL,
    backend=settings.CELERY_RESULT_BACKEND or settings.REDIS_URL,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    beat_schedule=getattr(settings, "CELERY_BEAT_SCHEDULE", {}),
)

# Optional: autodiscover tasks in core and plugins
celery_app.autodiscover_tasks([
    "core",
    "plugins",
])
