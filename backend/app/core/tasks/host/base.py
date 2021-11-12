from abc import ABC, abstractmethod

from app.core.host import connections


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
