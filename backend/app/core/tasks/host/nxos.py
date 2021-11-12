from app.core.tasks.host.base import Tasks
from app.settings import Settings, get_settings
from scrapli.response import Response

settings: Settings = get_settings()


class NXOSTasks(Tasks):
    async def update_network_interfaces_data(self) -> dict:
        async with self.connection.get_connection() as con:
            response: Response = await con.send_command("show interface")
        return_data = {}
        interfaces = response.genie_parse_output()
        if interfaces == []:
            return {}
        async for record in self.parse_show_interface(interfaces):
            return_data.update(record)
        return return_data
