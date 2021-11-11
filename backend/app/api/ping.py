from app.models.pong import Pong
from app.settings import Settings, get_settings
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/ping", response_model=Pong)
async def pong(settings: Settings = Depends(get_settings)):
    return {
        "ping": "pong",
        "project": settings.PROJECT,
        "environment": settings.ENVIRONMENT,
    }
