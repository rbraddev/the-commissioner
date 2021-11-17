from operator import or_
from typing import *

from sqlalchemy.sql.expression import except_

from app.core.inventory.tasks import update_inventory
from app.core.security.utils import get_current_user
from app.db import get_engine, get_session
from app.models.inventory import (
    Desktop,
    DesktopRead,
    DesktopReadWithInterface,
    Interface,
    Network,
    NetworkRead,
    NetworkReadWithInterfaces,
    SearchResults,
)
from app.models.auth import User
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import selectinload
from sqlmodel import Session, or_, select

router = APIRouter()


@router.post("/update/network", status_code=201)
async def start_network_update_task(user: User = Depends(get_current_user)):
    """
    Update network inventory DB from SW
    """
    if user["access_lvl"] < 5:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    await update_inventory(inventory_type="network")
    return {"message": "task completed"}


@router.post("/update/desktop", status_code=201)
async def start_desktop_update_task(user: User = Depends(get_current_user)):
    """
    Update desktop inventiry DB from SW
    """
    if user["access_lvl"] < 5:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    await update_inventory(inventory_type="desktop")
    return {"message": "task completed"}


@router.get("/network", response_model=List[NetworkReadWithInterfaces], status_code=200)
async def get_network_devices(
    site: str = None,
    device_type: str = None,
    nodeids: str = None,
    user: User = Depends(get_current_user)
):
    """
    Filter network devices
    """
    expression = None
    if nodeids:
        try:
            nodelist = [int(node) for node in nodeids.split(',')]
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="nodeid must be comma separated ids, e.g 100,101,102")
        expression = select(Network).options(selectinload(Network.interfaces)).where(Network.id.in_(nodelist))
    elif site is None and device_type is None:
        expression = select(Network).options(selectinload(Network.interfaces))
    elif site and device_type:
        expression = (
            select(Network)
            .options(selectinload(Network.interfaces))
            .where(
                Network.site.in_(site.split(",")),
                Network.device_type.in_(device_type.split(",")),
            )
        )
    elif site:
        expression = (
            select(Network)
            .options(selectinload(Network.interfaces))
            .where(Network.site.in_(site.split(",")))
        )
    elif device_type:
        expression = (
            select(Network)
            .options(selectinload(Network.interfaces))
            .where(Network.device_type.in_(device_type.split(",")))
        )

    with Session(get_engine()) as session:
        devices = session.exec(expression).all()
    return devices


@router.get("/desktop", response_model=List[DesktopReadWithInterface], status_code=200)
async def get_desktop_devices(
    site: str = None,
    nodeids: str = None,
    user: User = Depends(get_current_user)):
    """
    Filter desktops
    """
    expression = None
    if nodeids:
        try:
            nodelist = [int(node) for node in nodeids.split(',')]
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="nodeid must be comma separated ids, e.g 100,101,102")
        expression = select(Desktop).options(
            selectinload(Desktop.interface).selectinload(Interface.network_device)
        ).where(Desktop.id.in_(nodelist))
    elif site is None:
        expression = select(Desktop).options(
            selectinload(Desktop.interface).selectinload(Interface.network_device)
        )
    elif site:
        expression = (
            select(Desktop)
            .options(
                selectinload(Desktop.interface).selectinload(Interface.network_device)
            )
            .where(Desktop.site.in_(site.split(",")))
        )

    with Session(get_engine()) as session:
        devices = session.exec(expression).all()
    return devices


@router.get("/site", response_model=List[SearchResults], status_code=200)
async def get_site_devices(site: str = None, user: User = Depends(get_current_user)):
    """
    Get site inventory
    """
    if site is None:
        return []

    results = {"desktops": [], "network_devices": []}

    with Session(get_engine()) as session:
        desktops = session.exec(
            select(Desktop)
            .options(
                    selectinload(Desktop.interface).selectinload(
                        Interface.network_device
                    )
            )
            .where(Desktop.site == site)
        ).all()
        results.update({"desktops": desktops})

        network_devices = session.exec(
            select(Network).where(Network.site == site)
        ).all()
        results.update({"network_devices": network_devices})

    return [results]


@router.get("/search", response_model=List[SearchResults], status_code=200)
async def search_inventory(q: str = None, user: User = Depends(get_current_user)):
    """
    Search desktop and network inventory by hostname, ip or mac
    """
    results = {"desktops": [], "network_devices": [], "interfaces": []}
    if q:
        with Session(get_engine()) as session:
            desktops = session.exec(
                select(Desktop)
                .options(
                    selectinload(Desktop.interface).selectinload(
                        Interface.network_device
                    )
                )
                .where(
                    or_(
                        Desktop.hostname.ilike(f"%{q}%"),
                        Desktop.ip.ilike(f"%{q}%"),
                        Desktop.mac.ilike(f"%{q}%"),
                    )
                )
            ).all()
            results.update({"desktops": desktops})

            network_devices = session.exec(
                select(Network).where(
                    or_(
                        Network.hostname.ilike(f"%{q}%"),
                        Network.ip.ilike(f"%{q}%")
                    )
                )
            ).all()
            results.update({"network_devices": network_devices})
            interfaces = session.exec(
                select(Interface)
                .options(selectinload(Interface.network_device))
                .where(
                    or_(
                        Interface.ip.ilike(f"%{q}%"),
                        Interface.mac.ilike(f"%{q}%"),
                    )
                )
            ).all()
            results.update({"interfaces": interfaces})

    return [results]
