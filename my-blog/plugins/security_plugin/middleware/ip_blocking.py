from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import os

BLOCKED_IPS = os.getenv("BLOCKED_IPS", "").split(",") if os.getenv("BLOCKED_IPS") else []

class IPBlockingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        ip = request.client.host
        if ip in BLOCKED_IPS:
            return Response("IP blocked", status_code=403)
        return await call_next(request)
