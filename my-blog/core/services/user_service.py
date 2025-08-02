from core.models.user import User
from core.database import SessionLocal

def get_users():
    db = SessionLocal()
    users = db.query(User).all()
    db.close()
    return users
