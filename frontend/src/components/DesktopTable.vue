<template>
  <div>
    <q-table
      title="Desktops"
      :rows="rows"
      :columns="columns"
      row-key="hostname"
    />
  </div>
</template>

<script>
import { useStore } from 'vuex'
import { computed } from 'vue'

const columns = [
  {
    name: 'hostname',
    label: 'Hostname',
    align: 'left',
    field: row => row.hostname,
    format: val => val,
    sortable: true
  },
  {
    name: 'site',
    label: 'Site',
    align: 'left',
    field: row => row.site,
    format: val => val,
    sortable: true
  },
  {
    name: 'mac',
    label: 'MAC Address',
    align: 'left',
    field: row => row.mac,
    format: val => val,
    sortable: true
  },
  {
    name: 'ip',
    label: 'IP Address',
    align: 'left',
    field: row => row.ip,
    format: val => val,
    sortable: true
  },
  {
    name: 'cidr',
    label: 'Cidr',
    align: 'left',
    field: row => row.cidr,
    format: val => val ? `/${val}` : '',
    sortable: true
  },
  {
    name: 'switch',
    label: 'Switch',
    align: 'left',
    field: row => row.interface.network_device.hostname,
    format: val => val,
    sortable: true
  },
  {
    name: 'interface',
    label: 'Interface',
    align: 'left',
    field: row => row.interface.name,
    format: val => val,
    sortable: true
  }
]

export default {
  name: 'DesktopTable',

  setup () {
    const $store = useStore()

    const rows = computed(() => {
      return $store.state.inventory.desktop
    })

    return { rows, columns }
  }
}
</script>
