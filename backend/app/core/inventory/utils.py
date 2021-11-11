import re
from typing import *

from app.settings import Settings, get_settings
from httpx import AsyncClient, Response

settings: Settings = get_settings()


device_info = {
    "rt": {"device_type": "router", "platform": "ios"},
    "sw": {"device_type": "switch", "platform": "ios"},
    "nx": {"device_type": "nexus", "platform": "nxos"},
}


async def query_sw(query: str, parameters: dict) -> List[Dict[str, Any]]:
    headers = {"Content-Type": "application/json"}
    data = {
        "query": query,
        "parameters": parameters,
    }

    with AsyncClient() as client:
        response: Response = await client.get(
            f"https://{{settings.SW_HOST}}:17778/SolarWinds/InformationService/v3/Json/Query",
            headers=headers,
            auth=(settings.SW_USER, settings.SW_PASSWORD),
            verify=False,
            json=data,
        )

    if response.status_code != 200:
        return None

    return response["results"]


async def pull_network_inventory() -> List[Dict[str, Any]]:
    query = """SELECT NodeID as nodeid, IPAddress as ip, NodeName as hostname 
                FROM Orion.Nodes 
                WHERE NodeName LIKE @s OR NodeName LIKE @r OR NodeName LIKE @n"""
    parameters = {"s": "sw%", "r": "rt%", "n": "nx%"}

    # results = await query_sw(query, parameters)

    results = [
        {"nodeid": 1, "ip": "10.0.0.150", "hostname": "RT1001"},
        {"nodeid": 2, "ip": "10.0.0.151", "hostname": "RT1002"},
        {"nodeid": 3, "ip": "10.0.0.153", "hostname": "RT2001"},
        {"nodeid": 4, "ip": "10.0.0.154", "hostname": "RT2002"},
        {"nodeid": 5, "ip": "10.0.0.156", "hostname": "RT1011"},
        {"nodeid": 6, "ip": "10.0.0.157", "hostname": "RT1021"},
        {"nodeid": 7, "ip": "10.0.0.158", "hostname": "RT1031"},
        {"nodeid": 8, "ip": "10.0.0.159", "hostname": "SW1011"},
        {"nodeid": 9, "ip": "10.0.0.160", "hostname": "SW1021"},
        {"nodeid": 10, "ip": "10.0.0.161", "hostname": "SW1031"},
        {"nodeid": 11, "ip": "10.0.0.152", "hostname": "NX1001"},
        {"nodeid": 12, "ip": "10.0.0.155", "hostname": "NX2001"},
    ]

    for r in results:
        device = device_info.get(r["hostname"][:2].lower(), "undefined")
        r.update(
            {
                "active": True,
                "device_type": device["device_type"],
                "platform": device["platform"],
                "site": get_site(r["hostname"]),
            }
        )
    return results


async def pull_desktop_inventory() -> List[Dict[str, Any]]:
    query = """SELECT IPNode.IpNodeId as nodeid, IPNode.IPAddress as ip, Subnet.CIDR as cidr, IPNode.MAC as mac, IPNode.DhcpClientName as hostname
                FROM IPAM.IPNode
                INNER JOIN IPAM.Subnet ON IPNode.SubnetId = Subnet.SubnetId 
                WHERE DhcpClientName LIKE @d OR DhcpClientName LIKE @l"""
    parameters = {"d": "desktop%", "l": "laptop%"}

    # results = await query_sw(query, parameters)

    results = [
        {
            "nodeid": 1,
            "ip": "10.101.10.1",
            "cidr": 24,
            "mac": "52-54-00-1D-DA-08",
            "hostname": "PC1011.lab.local",
        },
        {
            "nodeid": 2,
            "ip": "10.101.10.2",
            "cidr": 24,
            "mac": "52-54-00-13-19-BF",
            "hostname": "PC1012.lab.local",
        },
        {
            "nodeid": 3,
            "ip": "10.102.10.1",
            "cidr": 24,
            "mac": "52-54-00-02-1D-EB",
            "hostname": "PC1021.lab.local",
        },
        {
            "nodeid": 4,
            "ip": "10.103.10.1",
            "cidr": 24,
            "mac": "52-54-00-1E-BF-5B",
            "hostname": "PC1031.lab.local",
        },
        {
            "nodeid": 5,
            "ip": "10.103.10.2",
            "cidr": 24,
            "mac": "52-54-00-1E-53-09",
            "hostname": "PC1032.lab.local",
        },
    ]

    if results:
        for r in results:
            r["mac"] = r["mac"].replace("-", "").lower()
            r["hostname"] = r["hostname"].split(".")[0]
            r.update({"site": get_site(r["hostname"]), "active": True})

    return results


def get_site(hostname: str) -> str:
    try:
        site = re.search(r"^\D+(\d{3})", hostname)[1]
    except TypeError:
        print(f"INVALID SITE: {hostname}")
        return "999"
    return site
