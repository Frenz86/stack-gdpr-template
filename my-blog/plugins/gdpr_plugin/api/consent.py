from fastapi import APIRouter

router = APIRouter()

@router.post("/give")
def give_consent():
    # Logic for giving consent
    return {"status": "consent given"}

@router.post("/withdraw")
def withdraw_consent():
    # Logic for withdrawing consent
    return {"status": "consent withdrawn"}
