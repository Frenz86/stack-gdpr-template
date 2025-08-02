from core.models.content import Content
from core.database import SessionLocal

def get_contents():
    db = SessionLocal()
    contents = db.query(Content).all()
    db.close()
    return contents
