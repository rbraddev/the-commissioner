import uvicorn
from fastapi import FastAPI

from app.api import inventory, ping


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(ping.router)
    application.include_router(
        inventory.router, prefix="/inventory", tags=["inventory"]
    )

    return application


app = create_application()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
