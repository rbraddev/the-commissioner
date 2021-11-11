from abc import ABC, abstractmethod

from app.core.host import connections


class Tasks(ABC):
    def __init__(self, connection: connections.Base):
        self.connection: connections.Base = connection

    @abstractmethod
    async def update_network_interfaces_data(self):
        pass
