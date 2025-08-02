from fastapi import FastAPI
from typing import Any

class BasePlugin:
    """
    Base class for all plugins. Ensures interface uniformity and security hooks.
    """
    name: str = "base"
    version: str = "1.0.0"
    enabled: bool = True

    def __init__(self, app: FastAPI, config: dict = None):
        self.app = app
        self.config = config or {}

    def load(self):
        """Load plugin and register routes/services."""
        pass

    def unload(self):
        """Unload plugin and cleanup resources."""
        pass

    def register_routes(self):
        """Register plugin-specific API routes."""
        pass

    def security_checks(self):
        """Run security and GDPR compliance checks."""
        pass
