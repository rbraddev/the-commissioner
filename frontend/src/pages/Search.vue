<template>
  <q-page>
    <SearchBar />
    <NetworkTable />
    <DesktopTable />
    <InterfaceTable />
  </q-page>
</template>

<script>
import SearchBar from 'components/SearchBar'
import NetworkTable from 'components/NetworkTable'
import DesktopTable from 'components/DesktopTable'
import InterfaceTable from 'components/InterfaceTable'
export default {
  name: 'Search',

  components: {
    SearchBar,
    NetworkTable,
    DesktopTable,
    InterfaceTable
  }
}
</script>
