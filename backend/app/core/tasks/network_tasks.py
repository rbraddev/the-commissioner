import asyncio
from typing import *

from app.core.host import Host
from app.core.tasks.tracker import TaskTracker, track
from app.db import get_engine, get_session
from app.models.inventory import Desktop, Interface, InterfaceCompare, Network
from jsondiff import diff
from scrapli.exceptions import ScrapliAuthenticationFailed
from sqlalchemy.orm import selectinload
# from sqlalchemy.future import select
from sqlmodel import Session, select


async def update_network_interfaces_task(nodeids: List[int], tracker: TaskTracker):
    with Session(get_engine()) as session:
        hosts = session.exec(select(Network).where(Network.nodeid.in_(nodeids))).all()

    await tracker.set_total(str(len(hosts)))

    tasks = [
        update_network_interfaces_run(
            Host(
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

    print(await tracker.getall())


@track
async def update_network_interfaces_run(host: Host, tracker: TaskTracker):
    try:
        for _ in range(3):
            results = await host.tasks.update_network_interfaces_data()
            if results != {}:
                break
            await asyncio.sleep(0.1)

        if results == {}:
            host.task_msg = "Failed retrieving data from device"
            await tracker.add_failed(host)
        else:
            await update_interfaces_db(host.nodeid, results)
    except (ScrapliAuthenticationFailed, OSError):
        host.task_msg = "Failed retrieving data from device"
        await tracker.add_failed(host)


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
                db_inf = next(
                    inf for inf in network_device.interfaces if inf.name == interface
                )
                updates = interface_updates(db_inf, data)
                print(updates)
                if updates:
                    for key, value in updates.items():
                        if key == "desktop":
                            if value:
                                desktop = session.exec(
                                    select(Desktop).where(Desktop.mac == value)
                                ).one()
                                desktop.interface = db_inf
                            else:
                                desktop = session.exec(
                                    select(Desktop).where(
                                        Desktop.id == db_inf.desktop[0].id
                                    )
                                ).one()
                                desktop.interface = None
                            session.add(desktop)
                        else:
                            setattr(db_inf, key, value)
                            session.add(db_inf)
                    session.commit()
            else:
                new_interface = Interface.parse_obj(data)
                new_interface.network_device = network_device
                session.add(new_interface)
                session.commit()
                session.refresh(new_interface)
                if data.get("desktop"):
                    desktop = session.exec(
                        select(Desktop).where(Desktop.mac == data.get("desktop"))
                    ).one()
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
    print(new_inf)
    print(db_inf)
    return diff(db_inf, new_inf)