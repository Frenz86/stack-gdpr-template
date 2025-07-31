# Service base Blog

from project_templates.blog.models.blog import BlogPost, BlogComment
from datetime import datetime

def get_all_posts():
    return [BlogPost(id=1, title="Hello World", content="Benvenuto nel blog!", author="admin", created_at=datetime.now())]

def get_all_comments():
    return [BlogComment(id=1, post_id=1, author="user", content="Ottimo articolo!", created_at=datetime.now())]
