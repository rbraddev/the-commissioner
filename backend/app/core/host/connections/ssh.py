from contextlib import asynccontextmanager
from typing import *  # noqa: F403

from app.core.host.connections import Base
from scrapli.driver.core import AsyncIOSXEDriver, AsyncNXOSDriver
from scrapli.driver.network.async_driver import AsyncNetworkDriver

PLATFORM = {"ios": AsyncIOSXEDriver, "nxos": AsyncNXOSDriver}


class SSH(Base):
    def __init__(self, host: str, username: str, password: str, platform: str, enable: str) -> None:
        self._con: AsyncNetworkDriver = None
        self.host: str = host
        self.username: str = username
        self.password: str = password
        self.enable: str = enable
        self.platform: str = platform

    def get_driver(self) -> None:
        self._con = PLATFORM.get(self.platform)(
            host=self.host,
            auth_username=self.username,
            auth_password=self.password,
            auth_secondary=self.enable,
            auth_strict_key=False,
            transport="asyncssh",
        )

    async def open(self):
        if self._con is None:
            self.get_driver()
        if not self._con.isalive():
            await self._con.open()

    async def close(self):
        await self._con.close()

    @asynccontextmanager
    async def get_connection(self):
        await self.open()
        yield self._con
        await self.close()

    @property
    def is_alive(self) -> bool:
        if self._con is not None:
            if self._con.isalive():
                return True
        return False

    # async def send_command(self, cmd: str, parse: bool = True) -> Union[Dict, str]:
    #     result = await self._con.send_command(cmd)
    #     if parse:
    #         return result.genie_parse_output()
    #     return result.result
