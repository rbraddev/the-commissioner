from ipaddress import IPv4Address
from typing import *

from pydantic import validator
from sqlmodel import Field, Relationship, SQLModel


class DeviceBase(SQLModel):
    hostname: str
    ip: str
    nodeid: int
    site: str

    @validator("ip")
    def must_be_an_ip(cls, v):
        IPv4Address(v)
        return v


class NetworkImport(DeviceBase):
    device_type: Optional[str]
    platform: Optional[str]
    active: Optional[bool]


class NetworkBase(NetworkImport):
    model: Optional[str]
    image: Optional[str]


class DesktopImport(DeviceBase):
    mac: str
    cidr: int
    active: Optional[bool]


class DesktopBase(DesktopImport):
    interface_id: Optional[int] = Field(default=None, foreign_key="interface.id")


class Network(NetworkBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    interfaces: List["Interface"] = Relationship(back_populates="network_device")


class NetworkRead(NetworkBase):
    id: int


class InterfaceBase(SQLModel):
    mac: str
    name: str
    description: Optional[str]
    vlan: Optional[int]
    cidr: Optional[int]

    network_device_id: Optional[int] = Field(default=None, foreign_key="network.id")


class Desktop(DesktopBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    interface: List["Interface"] = Relationship(back_populates="desktop")


class Interface(InterfaceBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    network_device: Optional[Network] = Relationship(back_populates="interfaces")
    desktop: Optional[Desktop] = Relationship(back_populates="interface")


class InterfaceRead(InterfaceBase):
    id: int


class InterfaceReadWithNetwork(InterfaceRead):
    network_device: NetworkRead


class NetworkReadWithInterfaces(NetworkRead):
    interfaces: Optional[List[InterfaceRead]] = []


class DesktopRead(DesktopBase):
    id: int


class DesktopReadWithInterface(DesktopRead):
    interface: InterfaceReadWithNetwork


class InterfaceReadWithDesktop(InterfaceBase):
    desktop: Optional[DesktopRead]
