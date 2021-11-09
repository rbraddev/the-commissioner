import uvicorn
from fastapi import FastAPI

from app.settings import get_settings, Settings
from app.api import inventory, ping, auth

settings: Settings = get_settings()


def create_application() -> FastAPI:
    application = FastAPI(title=settings.PROJECT)
    application.include_router(ping.router)
    application.include_router(
        inventory.router,
        prefix="/inventory",
        tags=["inventory"],
    )
    application.include_router(auth.router, prefix="/auth", tags=["auth"])

    return application


app = create_application()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
