from fastapi import APIRouter, Depends

from app.models.pong import Pong
from app.settings import Settings, get_settings

router = APIRouter()


@router.get("/ping", response_model=Pong)
async def pong(settings: Settings = Depends(get_settings)):
    return {
        "ping": "pong",
        "project": settings.PROJECT,
        "environment": settings.ENVIRONMENT,
    }
