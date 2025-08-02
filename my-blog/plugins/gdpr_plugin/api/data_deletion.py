from fastapi import APIRouter

router = APIRouter()

@router.delete("/")
def delete_data():
    # Logic for deleting user data
    return {"status": "data deleted"}
