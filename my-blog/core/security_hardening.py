"""
Security Hardening Priority Fixes

Best-practice security utilities for GDPR APIs and admin operations.
"""
from fastapi import HTTPException, Request, Depends
from pydantic import validator
import re
import redis
import time
import hashlib
import json
from datetime import datetime
from cryptography.fernet import Fernet
import os
import pyotp
import subprocess

# 1. Input Validation Middleware
class GDPRRequestValidator:
    @staticmethod
    def validate_user_id(user_id: str):
        if not re.match(r'^[a-f0-9-]{36}$', user_id):
            raise HTTPException(400, "Invalid user ID format")
        return user_id
    
    @staticmethod
    def validate_export_format(format: str):
        allowed = ['json', 'csv', 'xml']
        if format not in allowed:
            raise HTTPException(400, f"Format must be one of: {allowed}")
        return format

# 2. Rate Limiting for GDPR APIs
class GDPRRateLimitor:
    def __init__(self):
        self.redis = redis.Redis.from_url("redis://localhost:6379")
    
    async def check_rate_limit(self, request: Request, operation: str):
        user_id = request.headers.get("user-id")
        key = f"gdpr:{operation}:{user_id}"
        limits = {
            "export": (1, 3600),    # 1 per hour
            "deletion": (1, 86400), # 1 per day
            "breach": (5, 3600)     # 5 per hour
        }
        if operation in limits:
            count, window = limits[operation]
            current = self.redis.get(key)
            if current and int(current) >= count:
                raise HTTPException(429, f"Rate limit exceeded for {operation}")
            self.redis.incr(key)
            self.redis.expire(key, window)

# 3. Tamper-Proof Audit Logs
class TamperProofAuditLog:
    def __init__(self):
        self.last_hash = "0" * 64  # Genesis hash
    def log_gdpr_operation(self, operation: str, user_id: str, details: dict):
        timestamp = datetime.utcnow().isoformat()
        log_entry = {
            "timestamp": timestamp,
            "operation": operation,
            "user_id": user_id,
            "details": details,
            "previous_hash": self.last_hash
        }
        entry_string = json.dumps(log_entry, sort_keys=True)
        current_hash = hashlib.sha256(entry_string.encode()).hexdigest()
        log_entry["hash"] = current_hash
        self._store_audit_log(log_entry)
        self.last_hash = current_hash
        return log_entry
    def _store_audit_log(self, log_entry):
        # Implement DB or file storage here
        pass

# 4. Database Encryption at Rest
class GDPRDataEncryption:
    def __init__(self):
        key = os.getenv("GDPR_ENCRYPTION_KEY").encode()
        self.cipher = Fernet(key)
    def encrypt_sensitive_data(self, data: str) -> str:
        return self.cipher.encrypt(data.encode()).decode()
    def decrypt_sensitive_data(self, encrypted_data: str) -> str:
        return self.cipher.decrypt(encrypted_data.encode()).decode()

# 5. Admin 2FA for Critical Operations
class GDPRAdminSecurity:
    @staticmethod
    def verify_2fa_token(admin_id: str, token: str):
        secret = get_admin_2fa_secret(admin_id)
        totp = pyotp.TOTP(secret)
        if not totp.verify(token):
            raise HTTPException(403, "Invalid 2FA token")
        return True
    @staticmethod
    def require_2fa_for_deletion():
        def decorator(func):
            async def wrapper(*args, admin_id: str, token_2fa: str, **kwargs):
                GDPRAdminSecurity.verify_2fa_token(admin_id, token_2fa)
                return await func(*args, **kwargs)
            return wrapper
        return decorator

# 6. Backup Verification
class GDPRBackupSecurity:
    @staticmethod
    def create_verified_backup():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"gdpr_backup_{timestamp}.sql"
        subprocess.run([
            "pg_dump", 
            "--host=localhost", 
            "--dbname=stakc_app",
            f"--file={backup_file}"
        ])
        with open(backup_file, 'rb') as f:
            backup_hash = hashlib.sha256(f.read()).hexdigest()
        with open(f"{backup_file}.sha256", 'w') as f:
            f.write(f"{backup_hash}  {backup_file}")
        return backup_file, backup_hash
