import uvicorn
from app.api import auth, inventory, ping, tasks
from app.settings import Settings, get_settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

settings: Settings = get_settings()


def create_application() -> FastAPI:
    application = FastAPI(title=settings.PROJECT)

    origins = [
        "http://localhost:8080",
        "https://localhost:8080",
        "http://dashboard.networkdev.co.uk",
        "https://dashboard.networkdev.co.uk"
    ]
    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
    application.include_router(ping.router)
    application.include_router(
        inventory.router,
        prefix="/inventory",
        tags=["inventory"],
    )
    application.include_router(auth.router, prefix="/auth", tags=["auth"])
    application.include_router(tasks.router, prefix="/tasks", tags=["tasks"])

    return application


app = create_application()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
