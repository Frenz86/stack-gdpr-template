# core/api/blog_demo.py
"""
Blog Demo API endpoints for GDPR testing
Add this to your core/api/router.py
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
import json

router = APIRouter(prefix="/api/blog", tags=["Blog Demo"])

# Pydantic models for the blog demo
class UserCreate(BaseModel):
    email: EmailStr
    name: str
    consent_marketing: bool = False
    consent_analytics: bool = False

class UserOut(BaseModel):
    id: int
    email: str
    name: str
    created_at: str
    consent_marketing: bool
    consent_analytics: bool

class PostCreate(BaseModel):
    title: str
    content: str
    author_id: int
    tags: List[str] = []

class PostOut(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    author_name: str
    tags: List[str]
    created_at: str
    published: bool

class CommentCreate(BaseModel):
    post_id: int
    author_id: int
    content: str

class CommentOut(BaseModel):
    id: int
    post_id: int
    author_id: int
    author_name: str
    content: str
    created_at: str

# In-memory demo data (replace with real database in production)
DEMO_BLOG_DATA = {
    "users": [
        {
            "id": 1,
            "email": "john@demo.com",
            "name": "John Blogger",
            "created_at": "2024-01-01T10:00:00",
            "consent_marketing": True,
            "consent_analytics": True
        },
        {
            "id": 2,
            "email": "jane@demo.com", 
            "name": "Jane Writer",
            "created_at": "2024-01-15T14:30:00",
            "consent_marketing": False,
            "consent_analytics": True
        },
        {
            "id": 3,
            "email": "bob@demo.com",
            "name": "Bob Reader",
            "created_at": "2024-02-01T09:15:00",
            "consent_marketing": True,
            "consent_analytics": False
        }
    ],
    "posts": [
        {
            "id": 1,
            "title": "Welcome to Our GDPR-Compliant Blog!",
            "content": "This blog demonstrates full GDPR compliance with automatic consent management, data export, and privacy controls. Every user interaction is logged for transparency and compliance.",
            "author_id": 1,
            "author_name": "John Blogger",
            "tags": ["gdpr", "privacy", "compliance"],
            "created_at": "2024-01-01T12:00:00",
            "published": True
        },
        {
            "id": 2,
            "title": "Understanding Your Privacy Rights",
            "content": "Learn about your rights under GDPR: access, rectification, erasure, portability, and more. Our platform automatically handles all these requests.",
            "author_id": 1,
            "author_name": "John Blogger", 
            "tags": ["privacy", "rights", "education"],
            "created_at": "2024-01-10T15:30:00",
            "published": True
        },
        {
            "id": 3,
            "title": "Security Best Practices for Modern Web Apps",
            "content": "Exploring rate limiting, bot detection, and security headers that keep your applications safe while maintaining usability.",
            "author_id": 2,
            "author_name": "Jane Writer",
            "tags": ["security", "web", "best-practices"],
            "created_at": "2024-01-20T11:45:00",
            "published": True
        }
    ],
    "comments": [
        {
            "id": 1,
            "post_id": 1,
            "author_id": 2,
            "author_name": "Jane Writer",
            "content": "Great introduction to GDPR compliance! The automatic features are impressive.",
            "created_at": "2024-01-02T14:20:00"
        },
        {
            "id": 2,
            "post_id": 1,
            "author_id": 3,
            "author_name": "Bob Reader",
            "content": "Very helpful for understanding how data protection works in practice.",
            "created_at": "2024-01-03T09:30:00"
        },
        {
            "id": 3,
            "post_id": 2,
            "author_id": 3,
            "author_name": "Bob Reader",
            "content": "I used the data export feature - works perfectly!",
            "created_at": "2024-01-12T16:15:00"
        }
    ]
}

# Blog API Endpoints

@router.get("/posts", response_model=List[PostOut])
async def list_blog_posts(published_only: bool = True, limit: int = 10):
    """List blog posts with optional filtering"""
    posts = DEMO_BLOG_DATA["posts"]
    
    if published_only:
        posts = [p for p in posts if p["published"]]
    
    # Sort by created_at (newest first) and limit
    posts = sorted(posts, key=lambda x: x["created_at"], reverse=True)[:limit]
    
    return posts

@router.get("/posts/{post_id}", response_model=PostOut)
async def get_blog_post(post_id: int):
    """Get a specific blog post"""
    post = next((p for p in DEMO_BLOG_DATA["posts"] if p["id"] == post_id), None)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.post("/posts", response_model=PostOut)
async def create_blog_post(post: PostCreate):
    """Create a new blog post"""
    # Find author
    author = next((u for u in DEMO_BLOG_DATA["users"] if u["id"] == post.author_id), None)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    
    new_post = {
        "id": len(DEMO_BLOG_DATA["posts"]) + 1,
        "title": post.title,
        "content": post.content,
        "author_id": post.author_id,
        "author_name": author["name"],
        "tags": post.tags,
        "created_at": datetime.now().isoformat(),
        "published": True
    }
    
    DEMO_BLOG_DATA["posts"].append(new_post)
    return new_post

@router.get("/users", response_model=List[UserOut])
async def list_blog_users():
    """List all blog users"""
    return DEMO_BLOG_DATA["users"]

@router.get("/users/{user_id}", response_model=UserOut)
async def get_blog_user(user_id: int):
    """Get a specific user"""
    user = next((u for u in DEMO_BLOG_DATA["users"] if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/users", response_model=UserOut)
async def create_blog_user(user: UserCreate):
    """Create a new blog user with GDPR consent handling"""
    # Check if email already exists
    existing_user = next((u for u in DEMO_BLOG_DATA["users"] if u["email"] == user.email), None)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = {
        "id": len(DEMO_BLOG_DATA["users"]) + 1,
        "email": user.email,
        "name": user.name,
        "created_at": datetime.now().isoformat(),
        "consent_marketing": user.consent_marketing,
        "consent_analytics": user.consent_analytics
    }
    
    DEMO_BLOG_DATA["users"].append(new_user)
    
    # Auto-create GDPR consent records
    import httpx
    try:
        # Create marketing consent
        if user.consent_marketing:
            async with httpx.AsyncClient() as client:
                await client.post("http://localhost:8000/api/gdpr/consent", params={
                    "user_id": new_user["id"],
                    "consent_type": "marketing", 
                    "accepted": True
                })
        
        # Create analytics consent
        if user.consent_analytics:
            async with httpx.AsyncClient() as client:
                await client.post("http://localhost:8000/api/gdpr/consent", params={
                    "user_id": new_user["id"],
                    "consent_type": "analytics",
                    "accepted": True
                })
    except:
        # If GDPR API fails, continue anyway (for demo resilience)
        pass
    
    return new_user

@router.get("/posts/{post_id}/comments", response_model=List[CommentOut])
async def get_post_comments(post_id: int):
    """Get comments for a specific post"""
    comments = [c for c in DEMO_BLOG_DATA["comments"] if c["post_id"] == post_id]
    return sorted(comments, key=lambda x: x["created_at"])

@router.post("/posts/{post_id}/comments", response_model=CommentOut)
async def create_comment(post_id: int, comment: CommentCreate):
    """Create a new comment on a post"""
    # Verify post exists
    post = next((p for p in DEMO_BLOG_DATA["posts"] if p["id"] == post_id), None)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Verify author exists
    author = next((u for u in DEMO_BLOG_DATA["users"] if u["id"] == comment.author_id), None)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    
    new_comment = {
        "id": len(DEMO_BLOG_DATA["comments"]) + 1,
        "post_id": post_id,
        "author_id": comment.author_id,
        "author_name": author["name"],
        "content": comment.content,
        "created_at": datetime.now().isoformat()
    }
    
    DEMO_BLOG_DATA["comments"].append(new_comment)
    return new_comment

@router.get("/stats")
async def get_blog_stats():
    """Get blog statistics for dashboard"""
    total_posts = len(DEMO_BLOG_DATA["posts"])
    published_posts = len([p for p in DEMO_BLOG_DATA["posts"] if p["published"]])
    total_users = len(DEMO_BLOG_DATA["users"])
    total_comments = len(DEMO_BLOG_DATA["comments"])
    
    # Users with marketing consent
    marketing_consents = len([u for u in DEMO_BLOG_DATA["users"] if u["consent_marketing"]])
    analytics_consents = len([u for u in DEMO_BLOG_DATA["users"] if u["consent_analytics"]])
    
    return {
        "total_posts": total_posts,
        "published_posts": published_posts,
        "total_users": total_users,
        "total_comments": total_comments,
        "marketing_consents": marketing_consents,
        "analytics_consents": analytics_consents,
        "consent_rate_marketing": round((marketing_consents / max(total_users, 1)) * 100, 1),
        "consent_rate_analytics": round((analytics_consents / max(total_users, 1)) * 100, 1),
        "last_updated": datetime.now().isoformat()
    }

# GDPR integration endpoints for the blog
@router.get("/users/{user_id}/gdpr-export")
async def export_user_blog_data(user_id: int):
    """Export all blog data for a specific user (GDPR compliance)"""
    user = next((u for u in DEMO_BLOG_DATA["users"] if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Collect all user's blog data
    user_posts = [p for p in DEMO_BLOG_DATA["posts"] if p["author_id"] == user_id]
    user_comments = [c for c in DEMO_BLOG_DATA["comments"] if c["author_id"] == user_id]
    
    export_data = {
        "user_profile": user,
        "posts_authored": user_posts,
        "comments_made": user_comments,
        "blog_stats": {
            "total_posts": len(user_posts),
            "total_comments": len(user_comments),
            "member_since": user["created_at"]
        },
        "export_metadata": {
            "exported_at": datetime.now().isoformat(),
            "export_type": "blog_data",
            "gdpr_compliant": True
        }
    }
    
    return export_data

@router.delete("/users/{user_id}/gdpr-delete")
async def delete_user_blog_data(user_id: int, anonymize_content: bool = True):
    """Delete/anonymize user blog data (GDPR Right to Erasure)"""
    user = next((u for u in DEMO_BLOG_DATA["users"] if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if anonymize_content:
        # Anonymize user's posts and comments (keep content but remove personal data)
        for post in DEMO_BLOG_DATA["posts"]:
            if post["author_id"] == user_id:
                post["author_name"] = f"Anonymous User {user_id}"
        
        for comment in DEMO_BLOG_DATA["comments"]:
            if comment["author_id"] == user_id:
                comment["author_name"] = f"Anonymous User {user_id}"
        
        # Anonymize user profile
        user["email"] = f"deleted_user_{user_id}@anonymized.local"
        user["name"] = f"Anonymous User {user_id}"
        user["deleted_at"] = datetime.now().isoformat()
        
        return {
            "status": "anonymized",
            "user_id": user_id,
            "message": "User data has been anonymized while preserving content",
            "content_preserved": True
        }
    else:
        # Complete deletion (remove all user data)
        DEMO_BLOG_DATA["users"] = [u for u in DEMO_BLOG_DATA["users"] if u["id"] != user_id]
        DEMO_BLOG_DATA["posts"] = [p for p in DEMO_BLOG_DATA["posts"] if p["author_id"] != user_id]
        DEMO_BLOG_DATA["comments"] = [c for c in DEMO_BLOG_DATA["comments"] if c["author_id"] != user_id]
        
        return {
            "status": "deleted",
            "user_id": user_id,
            "message": "All user data has been permanently deleted",
            "content_preserved": False
        }

# Demo data seeding endpoint
@router.post("/demo/seed")
async def seed_demo_data():
    """Seed additional demo data for testing"""
    import random
    
    # Add more demo users
    for i in range(4, 8):
        new_user = {
            "id": i,
            "email": f"demo_user_{i}@example.com",
            "name": f"Demo User {i}",
            "created_at": datetime.now().isoformat(),
            "consent_marketing": random.choice([True, False]),
            "consent_analytics": random.choice([True, False])
        }
        DEMO_BLOG_DATA["users"].append(new_user)
    
    # Add more demo posts
    titles = [
        "Advanced GDPR Compliance Strategies",
        "Building Privacy-First Applications", 
        "Security Monitoring Best Practices",
        "User Consent Management Made Easy"
    ]
    
    for i, title in enumerate(titles, 4):
        new_post = {
            "id": i,
            "title": title,
            "content": f"This is demo content for {title}. It demonstrates how our GDPR-compliant blog system works with real data.",
            "author_id": random.choice([1, 2, 4, 5]),
            "author_name": f"Demo Author {random.randint(1, 5)}",
            "tags": random.sample(["gdpr", "privacy", "security", "compliance", "demo"], 2),
            "created_at": datetime.now().isoformat(),
            "published": True
        }
        DEMO_BLOG_DATA["posts"].append(new_post)
    
    return {
        "status": "seeded",
        "users_added": 4,
        "posts_added": 4,
        "message": "Demo data has been seeded successfully"
    }