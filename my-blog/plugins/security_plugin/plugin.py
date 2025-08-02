"""
🔒 Security Plugin - Production Ready
"""
from plugins.base_plugin import BasePlugin
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import time
import redis
from typing import Dict, Set
import logging

logger = logging.getLogger(__name__)

class SecurityPlugin(BasePlugin):
    name = "security_plugin"
    version = "1.0.0"
    required_permissions = ["database", "network"]
    
    def __init__(self, app: FastAPI, permissions: list):
        super().__init__(app, {})
        self.permissions = permissions
        self.redis_client = None
        self.rate_limits: Dict[str, int] = {}
        self.blocked_ips: Set[str] = set()
        
    async def initialize(self):
        """Initialize security plugin"""
        try:
            self.redis_client = redis.Redis.from_url("redis://redis:6379", decode_responses=True)
            self.redis_client.ping()
            logger.info("✅ Security plugin Redis connected")
        except Exception as e:
            logger.warning(f"⚠️ Security plugin Redis unavailable: {e}")
            
        # Add security middleware
        self.app.middleware("http")(self.security_middleware)
        logger.info("✅ Security middleware registered")
        
    def register_routes(self):
        """Register security API routes"""
        from fastapi import APIRouter
        
        router = APIRouter(prefix="/security", tags=["Security"])
        
        @router.get("/status")
        async def security_status():
            return {
                "status": "active",
                "rate_limiting": True,
                "bot_detection": True,
                "blocked_ips_count": len(self.blocked_ips),
                "rate_limits_active": len(self.rate_limits)
            }
            
        @router.get("/metrics")
        async def security_metrics():
            return {
                "blocked_requests": len(self.blocked_ips),
                "rate_limited_ips": len(self.rate_limits),
                "security_level": "high"
            }
            
        self.app.include_router(router)
        logger.info("✅ Security routes registered")
        
    async def security_middleware(self, request: Request, call_next):
        """Security middleware with rate limiting and bot detection"""
        client_ip = request.client.host
        user_agent = request.headers.get("user-agent", "")
        
        # Bot detection
        if self._is_bot(user_agent):
            logger.warning(f"🚫 Bot detected: {client_ip} - {user_agent}")
            return JSONResponse(
                status_code=403,
                content={"error": "Bot access denied"}
            )
            
        # Rate limiting
        if self._is_rate_limited(client_ip):
            logger.warning(f"⚡ Rate limited: {client_ip}")
            return JSONResponse(
                status_code=429,
                content={"error": "Rate limit exceeded"}
            )
            
        # Process request
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        
        # Add security headers
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["X-Response-Time"] = str(process_time)
        
        return response
        
    def _is_bot(self, user_agent: str) -> bool:
        """Simple bot detection"""
        bot_indicators = ["bot", "crawler", "spider", "python-requests", "curl"]
        return any(indicator in user_agent.lower() for indicator in bot_indicators)
        
    def _is_rate_limited(self, client_ip: str) -> bool:
        """Simple rate limiting (100 requests per minute)"""
        current_time = int(time.time() / 60)  # Current minute
        key = f"{client_ip}:{current_time}"
        
        if self.redis_client:
            try:
                count = self.redis_client.incr(key)
                if count == 1:
                    self.redis_client.expire(key, 60)
                return count > 100
            except:
                pass
                
        # Fallback to memory
        self.rate_limits[key] = self.rate_limits.get(key, 0) + 1
        return self.rate_limits.get(key, 0) > 100
        
    async def cleanup(self):
        """Cleanup security plugin"""
        if self.redis_client:
            self.redis_client.close()
        logger.info("✅ Security plugin cleaned up")
