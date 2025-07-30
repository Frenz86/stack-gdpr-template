from fastapi import FastAPI
from plugins.realtime_plugin.api import router

class RealtimePlugin:
    def __init__(self, app: FastAPI, permissions=None):
        self.app = app
        self.permissions = permissions or []

    def register_routes(self):
        self.app.include_router(router)

    async def initialize(self):
        pass

    async def cleanup(self):
        pass
