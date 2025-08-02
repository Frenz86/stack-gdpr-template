from fastapi import APIRouter, Depends
from core.schemas.content import ContentSchema
from core.services.content_service import get_contents

router = APIRouter()

@router.get("/", response_model=list[ContentSchema])
def list_contents():
    return get_contents()
