from ipaddress import IPv4Address
from typing import *

from pydantic import BaseModel, validator
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


class InterfaceBase(SQLModel):
    name: str
    mac: Optional[str]
    description: Optional[str]
    vlan: Optional[int]
    cidr: Optional[int]
    ip: Optional[str]

    network_device_id: Optional[int] = Field(default=None, foreign_key="network.id")


class Network(NetworkBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    interfaces: List["Interface"] = Relationship(back_populates="network_device")


class Desktop(DesktopBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    interface: Optional["Interface"] = Relationship(back_populates="desktop")


class Interface(InterfaceBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    network_device: Optional[Network] = Relationship(back_populates="interfaces")
    desktop: Optional[Desktop] = Relationship(back_populates="interface")


class NetworkRead(NetworkBase):
    id: int


class InterfaceRead(InterfaceBase):
    id: int


class NetworkReadWithInterfaces(NetworkRead):
    interfaces: Optional[List[InterfaceRead]] = []


class InterfaceReadWithNetwork(InterfaceRead):
    network_device: NetworkRead


class DesktopRead(DesktopBase):
    id: int


class DesktopReadWithInterface(DesktopRead):
    interface: Optional[InterfaceReadWithNetwork]


class InterfaceReadWithDesktop(InterfaceBase):
    desktop: Optional[DesktopRead]


class SearchResults(BaseModel):
    desktops: List[DesktopReadWithInterface] = []
    network_devices: List[NetworkRead] = []
    interfaces: List[InterfaceReadWithNetwork] = []


class InterfaceCompare(BaseModel):
    name: str
    description: Optional[str] = None
    ip: Optional[str] = None
    cidr: Optional[int] = None
    mac: Optional[str] = None
    vlan: Optional[int] = None
    desktop: Optional[str] = None
