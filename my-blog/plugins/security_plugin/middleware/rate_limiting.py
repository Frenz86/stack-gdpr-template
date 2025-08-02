
import asyncio
import json
import logging
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import time
import redis
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
r = redis.Redis.from_url(REDIS_URL)
RATE_LIMIT = 100  # richieste per IP ogni 60 secondi
WINDOW = 60
logger = logging.getLogger(__name__)

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 🚨 HOTFIX: Escludi health checks
        if request.url.path in ["/health", "/health/deep", "/metrics"]:
            return await call_next(request)
        # 🚨 HOTFIX: Gestione errori Redis
        try:
            ip = self.get_client_ip(request)
            key = f"rate:{ip}"
            # Check with timeout
            async with asyncio.timeout(1.0):  # 1 second timeout
                if await self.is_rate_limited(key):
                    return Response(
                        content=json.dumps({
                            "error": "Rate limit exceeded",
                            "retry_after": 60
                        }),
                        status_code=429,
                        headers={"Retry-After": "60"}
                    )
        except asyncio.TimeoutError:
            logger.warning("Rate limiting timeout - allowing request")
            # 🚨 FAIL OPEN: Se Redis è down, non bloccare
        except Exception as e:
            logger.error(f"Rate limiting error: {e}")
            # 🚨 FAIL OPEN: Se c'è errore, non bloccare
        return await call_next(request)

    async def is_rate_limited(self, key: str) -> bool:
        now = int(time.time())
        window_start = now - WINDOW
        r.zremrangebyscore(key, 0, window_start)
        r.zadd(key, {str(now): now})
        count = r.zcard(key)
        r.expire(key, WINDOW)
        return count > RATE_LIMIT

    def get_client_ip(self, request: Request) -> str:
        """HOTFIX: IP detection robusto."""
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        real_ip = request.headers.get("x-real-ip")
        if real_ip:
            return real_ip
        return request.client.host if request.client else "unknown"
