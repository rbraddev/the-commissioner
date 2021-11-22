<template>
  <q-page>
    <div>
      <SearchBar />
    </div>
    <div v-if="network.length > 0" class="q-my-md">
      <NetworkTable />
    </div>
    <div v-if="desktop.length > 0" class="q-my-md">
      <DesktopTable />
    </div>
    <div v-if="interfaces.length > 0" class="q-my-md">
      <InterfaceTable />
    </div>
  </q-page>
</template>

<script>
import { useStore } from 'vuex'
import { computed } from 'vue'

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
  },

  setup () {
    const $store = useStore()

    const network = computed(() => $store.state.inventory.network)
    const desktop = computed(() => $store.state.inventory.desktop)
    const interfaces = computed(() => $store.state.inventory.interfaces)

    return { network, desktop, interfaces }
  }
}
</script>
