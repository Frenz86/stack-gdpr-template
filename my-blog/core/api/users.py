from fastapi import APIRouter, Depends
from core.schemas.user import UserSchema
from core.services.user_service import get_users

router = APIRouter()

@router.get("/", response_model=list[UserSchema])
def list_users():
    return get_users()
