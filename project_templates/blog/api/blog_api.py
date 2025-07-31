# API base Blog

from fastapi import APIRouter
from project_templates.blog.models.blog import BlogPost, BlogComment
from datetime import datetime

router = APIRouter()

@router.get("/posts", response_model=list[BlogPost])
def list_posts():
    # Dummy data
    return [BlogPost(id=1, title="Hello World", content="Benvenuto nel blog!", author="admin", created_at=datetime.now())]

@router.get("/comments", response_model=list[BlogComment])
def list_comments():
    # Dummy data
    return [BlogComment(id=1, post_id=1, author="user", content="Ottimo articolo!", created_at=datetime.now())]
