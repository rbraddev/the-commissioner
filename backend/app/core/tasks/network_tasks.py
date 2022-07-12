import asyncio
from typing import *

from app.core.host import Host
from app.core.tasks.tracker import TaskTracker, track, track_task, end_task
from app.db import get_engine, get_session
from app.models.inventory import Desktop, Interface, InterfaceCompare, Network
from jsondiff import diff
from scrapli.exceptions import ScrapliAuthenticationFailed
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from app.settings import Settings, get_settings

settings: Settings = get_settings()


@track_task
async def update_network_interfaces_task(nodeids: List[int], tracker: TaskTracker):
    await tracker.set_status("Running")
    with Session(get_engine()) as session:
        hosts = session.exec(select(Network).where(Network.nodeid.in_(nodeids))).all()

    await tracker.set_total(len(hosts))

    tasks = [
        update_network_interfaces_device(
            host=Host(
                hostname=host.hostname,
                ip=host.ip,
                platform=host.platform,
                device_type=host.device_type,
                nodeid=host.nodeid,
            ),
            tracker=tracker,
        )
        for host in hosts
    ]

    await asyncio.gather(*tasks)


@track
async def update_network_interfaces_device(host: Host, tracker: TaskTracker):
    try:
        for _ in range(3):
            results = await host.tasks.update_network_interfaces_data()
            if results != {}:
                break
            await asyncio.sleep(0.2)

        if results == {}:
            raise ValueError("Unable to get data from device")
        else:
            await update_interfaces_db(host.nodeid, results)
    except (ScrapliAuthenticationFailed, OSError) as exc:
        raise ConnectionError(exc)


async def update_interfaces_db(nodeid: int, interfaces: dict):
    with Session(get_engine()) as session:
        network_device = session.exec(
            select(Network)
            .options(selectinload(Network.interfaces).selectinload(Interface.desktop))
            .where(Network.nodeid == nodeid)
        ).one()
        for interface, data in interfaces.items():
            data.update({"name": interface})
            if interface in (inf.name for inf in network_device.interfaces):
                db_inf = next(inf for inf in network_device.interfaces if inf.name == interface)
                updates = interface_updates(db_inf, data)
                if updates:
                    for key, value in updates.items():
                        if key == "desktop":
                            if value:
                                desktop = session.exec(select(Desktop).where(Desktop.mac == value)).one()
                                desktop.interface = db_inf
                            else:
                                desktop = session.exec(select(Desktop).where(Desktop.id == db_inf.desktop[0].id)).one()
                                desktop.interface = None
                            session.add(desktop)
                        else:
                            setattr(db_inf, key, value)
                            session.add(db_inf)
                    session.commit()
            else:
                desktop = data.pop("desktop", None)
                new_interface = Interface.parse_obj(data)
                new_interface.network_device = network_device
                session.add(new_interface)
                session.commit()
                session.refresh(new_interface)
                if desktop:
                    desktop = session.exec(select(Desktop).where(Desktop.mac == desktop)).one()
                    desktop.interface = new_interface
                    session.add(desktop)
                    session.commit()


def interface_updates(in_db, current):

    new_inf = InterfaceCompare.parse_obj(
        {
            "name": current.get("name"),
            "description": current.get("description"),
            "mac": current.get("mac"),
            "ip": current.get("ip"),
            "cidr": current.get("cidr"),
            "vlan": current.get("vlan"),
            "desktop": current.get("desktop"),
        }
    ).dict()
    db_inf = InterfaceCompare.parse_obj(
        {
            "name": in_db.name,
            "description": in_db.description,
            "mac": in_db.mac,
            "ip": in_db.ip,
            "cidr": in_db.cidr,
            "vlan": in_db.vlan,
            "desktop": in_db.desktop[0].mac if in_db.desktop else None,
        }
    ).dict()
    return diff(db_inf, new_inf)


@track_task
async def deactivate_site_task(site: str, tracker: TaskTracker):
    with Session(get_engine()) as session:
        hosts = session.exec(select(Network).where(Network.site == site, Network.device_type == "switch")).all()

    if hosts == []:
        raise ValueError("No hosts found")

    await tracker.set_total(len(hosts))

    tasks = [
        deactivate_site_device(
            host=Host(
                hostname=host.hostname,
                ip=host.ip,
                platform=host.platform,
                device_type=host.device_type,
                nodeid=host.nodeid,
            ),
            tracker=tracker,
        )
        for host in hosts
    ]
    asyncio.gather(*tasks)


@track
async def deactivate_site_device(host: Host, tracker: TaskTracker):
    await host.tasks.shutdown_interface([f"vlan{vlan}" for vlan in settings.SITE_VLANS])


@track_task
async def activate_site_task(site: str, tracker: TaskTracker):
    with Session(get_engine()) as session:
        hosts = session.exec(select(Network).where(Network.site == site, Network.device_type == "switch")).all()

    if hosts == []:
        raise ValueError("No hosts found")

    await tracker.set_total(len(hosts))

    tasks = [
        activate_site_device(
            host=Host(
                hostname=host.hostname,
                ip=host.ip,
                platform=host.platform,
                device_type=host.device_type,
                nodeid=host.nodeid,
            ),
            tracker=tracker,
        )
        for host in hosts
    ]
    asyncio.gather(*tasks)


@track
async def activate_site_device(host: Host, tracker: TaskTracker):
    await host.tasks.enable_interface([f"vlan{vlan}" for vlan in settings.SITE_VLANS])


@track_task
async def get_site_status_task(site: str, tracker: TaskTracker):
    with Session(get_engine()) as session:
        hosts = session.exec(select(Network).where(Network.site == site, Network.device_type == "switch")).all()

    if hosts == []:
        raise ValueError("No hosts found")

    await tracker.set_total(len(hosts))

    tasks = [
        get_site_status_host(
            host=Host(
                hostname=host.hostname,
                ip=host.ip,
                platform=host.platform,
                device_type=host.device_type,
                nodeid=host.nodeid,
            ),
            tracker=tracker,
        )
        for host in hosts
    ]
    asyncio.gather(*tasks)


@track
async def get_site_status_host(host: Host, tracker: TaskTracker):
    host.result = await host.tasks.interface_vlan_status([f"Vlan{vlan}" for vlan in settings.SITE_VLANS])
