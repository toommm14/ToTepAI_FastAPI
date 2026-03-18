from fastapi import FastAPI

from routers.harvest_router import router as harvest_router


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


server = FastAPIServer()
app = server.app