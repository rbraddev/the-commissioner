from typing import *

from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.inventory.tasks import update_inventory
from app.db import get_session

router = APIRouter()


@router.post("/update/network", status_code=201)
async def start_update_task():
    await update_inventory(inventory_type="network")
    return {"message": "task completed"}


@router.post("/update/desktop", status_code=201)
async def start_update_task():
    await update_inventory(inventory_type="desktop")
    return {"message": "task completed"}
