from ipaddress import AddressValueError, IPv4Address
from typing import *

from app.core.host.connections.ssh import PLATFORM, SSH
from app.core.host.credentials import Credentials
from app.core.host.errors import (InvalidIPAddress, InvalidPlatform,
                                  NoTaskListFound)
from app.core.tasks.host import IOSRTTasks, IOSSWTasks, NXOSTasks
from app.core.tasks.host.base import Tasks
from app.settings import Settings, get_settings

settings: Settings = get_settings()


class Host:
    def __init__(
        self, hostname: str, ip: str, platform: str, device_type: str, nodeid: int
    ) -> None:
        if platform not in PLATFORM.keys():
            raise InvalidPlatform(
                f"Host {hostname}: platform must be {list(PLATFORM.keys())}"
            )
        self.hostname: str = hostname
        try:
            self.ip: str = str(IPv4Address(ip))
        except AddressValueError:
            raise InvalidIPAddress(
                f"Host: {hostname} - has an invalid ip address of {ip}"
            )
        self.platform: str = platform
        self.device_type: str = device_type
        self.nodeid: int = nodeid
        self.credentials: Credentials = Credentials(
            settings.API_USER, settings.API_PASSWORD
        )
        self.connection: SSH = None
        self.tasks: Tasks = None
        self.failed_msg: str = None
        self.result: Union[str, int, dict] = None

        self.set_connection()
        self.set_tasks()

    def set_tasks(self):
        if self.device_type == "router" and self.platform == "ios":
            self.tasks = IOSRTTasks(connection=self.connection)
        elif self.device_type == "switch" and self.platform == "ios":
            self.tasks = IOSSWTasks(connection=self.connection)
        elif self.platform == "nxos":
            self.tasks = NXOSTasks(connection=self.connection)
        else:
            raise NoTaskListFound(
                f"Unable to load task list for: {self.device_type} - {self.platform}"
            )

    def __repr__(self) -> str:
        return f"Host(Hostname: {self.hostname}, IP: {self.ip})"

    def __eq__(self, other) -> bool:
        return all(
            [
                self.__class__ == other.__class__,
                self.ip == other.ip,
            ]
        )

    def __hash__(self):
        return hash(self.ip)

    def failed_dict(self) -> dict:
        return {
            "hostname": self.hostname,
            "ip": self.ip,
            "nodeid": self.nodeid,
            "failed_msg": self.task_msg,
        }

    def result_dict(self) -> dict:
        return {
            "hostname": self.hostname,
            "ip": self.ip,
            "nodeid": self.nodeid,
            "result": self.result,
        }

    def set_connection(self):
        self.connection = SSH(
            host=self.ip,
            username=self.credentials.username,
            password=self.credentials.password,
            enable=self.credentials.enable,
            platform=self.platform,
        )
