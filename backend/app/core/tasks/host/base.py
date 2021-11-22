from typing import *
from abc import ABC, abstractmethod

from app.core.host import connections
from app.core.utils import render_file


class Tasks(ABC):
    def __init__(self, connection: connections.Base):
        self.connection: connections.Base = connection

    @abstractmethod
    async def update_network_interfaces_data(self):
        pass

    @staticmethod
    async def parse_show_interface(data: dict) -> dict:
        for k, v in data.items():
            ip = v["ipv4"][next(iter(v["ipv4"]))] if v.get("ipv4") else {}
            yield {
                k: {
                    "description": v.get("description"),
                    "mac": v.get("phys_address").replace(".", "")
                    if v.get("phys_address")
                    else None,
                    "ip": ip.get("ip"),
                    "cidr": int(ip.get("prefix_length"))
                    if ip.get("prefix_length")
                    else None,
                }
            }

    @staticmethod
    async def parse_show_vlan(data: dict) -> tuple:
        for k, v in data.items():
            if v.get("interfaces"):
                for interface in v["interfaces"]:
                    yield (interface, {"vlan": int(k)})

    @staticmethod
    async def parse_show_mac(data: dict) -> tuple:
        for k, v in data.items():
            yield (next(iter(v["interfaces"])), {"desktop": k.replace(".", "")})

    async def _send_config(self, config: str):
        async with self.connection.get_connection() as con:
            await con.send_configs(config.split("\n"))
    
    async def _send_command(self, cmd: str, parse: bool = True):
        async with self.connection.get_connection() as con:
            response = await con.send_command(cmd)
        return response.genie_parse_output() if parse else response.result

    async def shutdown_interface(self, interfaces: List[str]):
        config = render_file("shutdown_interface.j2", interfaces=interfaces)
        await self._send_config(config)

    async def enable_interface(self, interfaces: List[str]):
        config = render_file("enable_interface.j2", interfaces=interfaces)
        await self._send_config(config)
    
    async def interface_vlan_status(self, interfaces: List[str]):
        result = await self._send_command("show ip interface brief")        
        return {vlan: data["status"] for vlan, data in result["interface"].items() if vlan in interfaces}
