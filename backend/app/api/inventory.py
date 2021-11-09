from operator import or_
from typing import *

from fastapi import APIRouter, Depends
from sqlalchemy.future import select
from sqlalchemy import or_

from app.core.inventory.tasks import update_inventory
from app.core.security.utils import get_current_user
from app.db import get_session
from app.models.inventory import (
    NetworkRead,
    Network,
    Desktop,
    DesktopRead,
    SearchResults,
)
from app.models.token import User

router = APIRouter()


@router.post("/update/network", status_code=201)
async def start_network_update_task(current_user: User = Depends(get_current_user)):
    """
    Update network inventory DB from SW
    """
    await update_inventory(inventory_type="network")
    return {"message": "task completed"}


@router.post("/update/desktop", status_code=201)
async def start_desktop_update_task(current_user: User = Depends(get_current_user)
):
    """
    Update desktop inventiry DB from SW
    """
    await update_inventory(inventory_type="desktop")
    return {"message": "task completed"}


@router.get("/network", response_model=List[NetworkRead], status_code=200)
async def get_network_devices(
    site: str = None,
    device_type: str = None,
):  
    """
    Filter network devices
    """
    expression = None
    if site is None and device_type is None:
        expression = select(Network)
    elif site and device_type:
        expression = select(Network).where(
            Network.site.in_(site.split(",")),
            Network.device_type.in_(device_type.split(",")),
        )
    elif site:
        expression = select(Network).where(Network.site.in_(site.split(",")))
    elif device_type:
        expression = select(Network).where(
            Network.device_type.in_(device_type.split(","))
        )

    async with get_session() as session:
        results = await session.execute(expression)
        devices = results.scalars().all()
    return devices


@router.get("/desktop", response_model=List[DesktopRead], status_code=200)
async def get_desktop_devices(
    site: str = None,
):
    """
    Filter desktops
    """
    expression = None
    if site is None:
        expression = select(Desktop)
    elif site:
        expression = select(Desktop).where(Desktop.site.in_(site.split(",")))

    async with get_session() as session:
        results = await session.execute(expression)
        devices = results.scalars().all()
    return devices


@router.get("/site", response_model=List[SearchResults], status_code=200)
async def get_site_devices(
    site: str = None,
):
    """
    Get site inventory
    """
    if site is None:
        return []
    
    results = {"desktops": [], "network_devices": []}
    
    async with get_session() as session:
        desktop_results = await session.execute(select(Desktop).where(Desktop.site == site))
        desktops = desktop_results.scalars().all()
        results.update({"desktops": desktops})

        network_device_results = await session.execute(select(Network).where(Network.site == site))
        network_devices = network_device_results.scalars().all()
        results.update({"network_devices": network_devices})
    
    return [results]


@router.get("/search", response_model=List[SearchResults], status_code=200)
async def search_inventory(q: str = None):
    """
    Search desktop and network inventory by hostname, ip or mac
    """
    results = {"desktops": [], "network_devices": []}
    if q:
        async with get_session() as session:
            desktop_results = await session.execute(
                select(Desktop).where(
                    or_(
                        Desktop.hostname.ilike(f"%{q}%"),
                        Desktop.ip.ilike(f"%{q}%"),
                        Desktop.mac.ilike(f"%{q}%"),
                    )
                )
            )
            desktops = desktop_results.scalars().all()
            results.update({"desktops": desktops})

            network_device_results = await session.execute(
                select(Network).where(
                    or_(
                        Network.hostname.ilike(f"%{q}%"),
                    )
                )
            )
            network_devices = network_device_results.scalars().all()
            results.update({"network_devices": network_devices})

    return [results]
