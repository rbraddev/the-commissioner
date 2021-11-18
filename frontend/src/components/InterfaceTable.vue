<template>
  <div>
    <q-table
      title="Interfaces"
      :rows="rows"
      :columns="columns"
      row-key="id"
    />
  </div>
</template>

<script>
import { useStore } from 'vuex'
import { computed } from 'vue'

const columns = [
  {
    name: 'name',
    label: 'Interface',
    align: 'left',
    field: row => row.name,
    format: val => val,
    sortable: true
  },
  {
    name: 'description',
    label: 'Description',
    align: 'left',
    field: row => row.description,
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
    name: 'device',
    label: 'Network Device',
    align: 'left',
    field: row => row.network_device.hostname,
    format: val => val,
    sortable: true
  }
]

export default {
  name: 'InterfaceTable',

  setup () {
    const $store = useStore()

    const rows = computed(() => {
      return $store.state.inventory.interfaces
    })

    return { rows, columns }
  }
}
</script>
