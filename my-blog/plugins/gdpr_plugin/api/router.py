from fastapi import APIRouter
from .consent import router as consent_router
from .data_export import router as export_router
from .data_deletion import router as deletion_router
from .admin import router as admin_router

router = APIRouter()
router.include_router(consent_router, prefix="/consent", tags=["Consent"])
router.include_router(export_router, prefix="/export", tags=["Data Export"])
router.include_router(deletion_router, prefix="/deletion", tags=["Data Deletion"])
router.include_router(admin_router, prefix="/admin", tags=["GDPR Admin"])
