<template>
  <div>
    <q-table
      title="Network Devices"
      :rows="rows"
      :columns="networkColumns"
      row-key="hostname"
      :pagination="networkPagination"
    >
      <template v-slot:header="props">
        <q-tr :props="props">
          <q-th auto-width />
          <q-th
            v-for="col in props.cols"
            :key="col.name"
            :props="props"
          >
            {{ col.label }}
          </q-th>
        </q-tr>
      </template>
      <template v-slot:body="props">
        <q-tr :props="props">
          <q-td auto-width>
            <q-btn
              size="sm"
              color="primary"
              round
              dense
              @click="rowClick(props)"
              :icon="props.expand ? 'remove' : 'add'"
            />
          </q-td>
          <q-td
            v-for="col in props.cols"
            :key="col.name"
            :props="props"
          >
            {{ col.value }}
          </q-td>
        </q-tr>
        <q-tr v-show="props.expand" :props="props">
          <q-td colspan="100%">
            <q-table
              :rows="props.row.interfaces"
              :columns="interfaceColumns"
              :hide-bottom="interfaceHideBottom"
              :pagination="interfacePagination"
            />
          </q-td>
        </q-tr>
      </template>
    </q-table>
  </div>
</template>

<script>
import { useStore } from 'vuex'
import { computed, ref } from 'vue'
const networkColumns = [
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
    name: 'device_type',
    label: 'Device Type',
    align: 'left',
    field: row => row.device_type,
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
  }
]

const interfaceColumns = [
  {
    name: 'interface',
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
    name: 'vlan',
    label: 'VLAN',
    align: 'left',
    field: row => row.vlan,
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
  }
]

export default {
  name: 'NetworkTable',

  setup () {
    const $store = useStore()
    const interfaceHideBottom = ref(true)
    const networkPagination = ref({ rowsPerPage: 20 })
    const interfacePagination = ref({ rowsPerPage: 1000 })

    const rows = computed(() => {
      return $store.state.inventory.network
    })

    const rowClick = (props) => {
      props.expand = !props.expand
      if (props.expand === true && props.row.interfaces === undefined) {
        $store.dispatch('inventory/getNetwork', props.row.id)
      }
    }

    return { rows, networkColumns, rowClick, interfaceColumns, interfaceHideBottom, interfacePagination, networkPagination }
  }
}
</script>
