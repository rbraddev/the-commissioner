from app.core.tasks.host.base import Tasks
from app.settings import Settings, get_settings
from scrapli.response import MultiResponse

settings: Settings = get_settings()


class IOSSWTasks(Tasks):
    async def update_network_interfaces_data(self) -> dict:
        async with self.connection.get_connection() as con:
            response: MultiResponse = await con.send_commands(
                ["show interfaces", "show vlan", "show mac address-table"]
            )

        return_data = {}
        interfaces = response[0].genie_parse_output()
        if interfaces == []:
            return {}
        async for record in self.parse_show_interface(interfaces):
            return_data.update(record)

        vlans = response[1].genie_parse_output()
        if vlans == []:
            return {}
        async for record in self.parse_show_vlan(vlans["vlans"]):
            return_data[record[0]].update(record[1])

        macs = response[2].genie_parse_output()
        if macs == []:
            return {}
        async for record in self.parse_show_mac(macs["mac_table"]["vlans"][str(settings.DATA_VLAN)]["mac_addresses"]):
            return_data[record[0]].update(record[1])

        return return_data
