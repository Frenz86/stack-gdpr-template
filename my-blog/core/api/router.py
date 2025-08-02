from fastapi import APIRouter
from core.api.users import router as users_router
from core.api.content import router as content_router
from core.api.health import router as health_router

router = APIRouter()
router.include_router(users_router, prefix="/users", tags=["users"])
router.include_router(content_router, prefix="/content", tags=["content"])
router.include_router(health_router, prefix="/health", tags=["health"])
