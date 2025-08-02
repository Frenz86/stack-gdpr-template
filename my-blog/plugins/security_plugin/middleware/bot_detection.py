from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import re

BOT_USER_AGENTS = [
    r"bot", r"spider", r"crawl", r"python-requests", r"wget", r"curl"
]

class BotDetectionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        ua = request.headers.get("user-agent", "").lower()
        if any(re.search(bot, ua) for bot in BOT_USER_AGENTS):
            return Response("Bot detected", status_code=403)
        return await call_next(request)
