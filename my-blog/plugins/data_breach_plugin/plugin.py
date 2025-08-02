from plugins.base_plugin import BasePlugin
from fastapi import FastAPI, APIRouter

class DataBreachPlugin(BasePlugin):
    name = "data_breach"
    version = "1.0.0"

    def load(self):
        self.register_routes()

    def register_routes(self):
        router = APIRouter(prefix="/breach", tags=["Data Breach"])

        @router.post("/notify")
        def notify_breach(description: str):
            # Qui si integrerebbe la notifica a utenti/DPO
            return {"status": "notified", "description": description}

        self.app.include_router(router)
