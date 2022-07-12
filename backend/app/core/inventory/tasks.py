import logging

from app.core.inventory.utils import pull_desktop_inventory, pull_network_inventory
from app.db import get_session
from app.models.inventory import Desktop, DesktopImport, Network, NetworkImport
from jsondiff import diff
from sqlalchemy.future import select
from sqlmodel.main import SQLModelMetaclass

log = logging.getLogger("uvicorn")

inventory_dict = {
    "network": {
        "inventory": pull_network_inventory,
        "keys": ["nodeid", "ip", "hostname", "device_type", "platform", "active"],
        "node_type": Network,
        "import_model": NetworkImport,
    },
    "desktop": {
        "inventory": pull_desktop_inventory,
        "keys": ["nodeid", "ip", "cidr", "mac", "hostname", "active"],
        "node_type": Desktop,
        "import_model": DesktopImport,
    },
}


async def update_inventory(inventory_type: str) -> None:
    """Pulls network and desktop inventory from Solarwinds"""
    if inventory_type not in ["network", "desktop"]:
        raise ValueError("Inventory must be of type 'network' or 'desktop'")

    inventory: dict = inventory_dict.get(inventory_type)

    sw_inventory: list = await inventory["inventory"]()

    async with get_session() as session:
        results: list = await session.execute(select(inventory["node_type"]))
        db_inventory = [inventory["import_model"].from_orm(item).dict() for item in results.scalars().all()]

    for sw_device in sw_inventory:
        if sw_device["nodeid"] not in (device["nodeid"] for device in db_inventory):
            await add_device(sw_device, inventory["node_type"])
            continue

        try:
            db_device = next(device for device in db_inventory if device["nodeid"] == sw_device["nodeid"])
            await update_device(sw_device, db_device, inventory["node_type"])
            continue
        except StopIteration:
            pass

    for db_device in db_inventory:
        if db_device["nodeid"] not in (device["nodeid"] for device in sw_inventory):
            await set_inactive(db_device, inventory["node_type"])


async def add_device(device: dict, model: SQLModelMetaclass):
    async with get_session() as session:
        new_device = model.parse_obj(device)
        session.add(new_device)
        await session.commit()


async def update_device(sw_device: dict, db_device: dict, model: SQLModelMetaclass):
    updates = diff(db_device, sw_device)
    async with get_session() as session:
        results = await session.execute(select(model).where(model.nodeid == db_device["nodeid"]))
        device = results.scalars().one()
        for key, value in updates.items():
            setattr(device, key, value)
        session.add(device)
        await session.commit()


async def set_inactive(device: dict, model: SQLModelMetaclass):
    async with get_session() as session:
        results = await session.execute(select(model).where(model.nodeid == device["nodeid"]))
        device = results.scalars().one()
        device.active = False
        session.add(device)
        await session.commit()
