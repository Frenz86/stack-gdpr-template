# Core validators for GDPR compliance and business logic

import re
from typing import Any

def validate_email(email: str) -> bool:
    """Basic email format validation."""
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None

def validate_uuid(uuid_str: str) -> bool:
    """Validate if string is a valid UUID."""
    import uuid
    try:
        uuid.UUID(uuid_str)
        return True
    except ValueError:
        return False

def validate_consent(consent: dict) -> bool:
    """Validate consent dictionary for GDPR compliance."""
    required_fields = ["user_id", "consent_type", "timestamp"]
    return all(field in consent for field in required_fields)

# Add more validators as needed for GDPR, security, etc.
