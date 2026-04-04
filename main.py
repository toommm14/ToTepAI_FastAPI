from fastapi import FastAPI

try:
    from dotenv import load_dotenv

    load_dotenv()
except Exception:
    pass

from routers.harvest_router import router as harvest_router
from routers.harvest_session_router import router as harvest_session_router


class FastAPIServer:

    def __init__(self):             

        self.app = FastAPI(
            title="ToTepAI Harvest API",
            description="API for receiving harvest classification data from Orange Pi",
            version="1.0"
        )

        self.register_routes()


    def register_routes(self):

        self.app.include_router(harvest_router)
        self.app.include_router(harvest_session_router)


server = FastAPIServer()
app = server.app