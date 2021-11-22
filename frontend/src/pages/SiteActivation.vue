<template>
  <q-page padding>
    <div class="text-h5">
      Site Activation/Deactivation
    </div>
    <div class="row no-wrap">
      <q-select v-model="site" :options="sites" label="Select Site" class="col-10 q-mr-md" />
      <q-btn :disabled="btnDisabled" class="col-2 bg-primary text-white" @click="runTask">{{ btnLabel }}</q-btn>
    </div>
    <div v-if="siteSwitches !== undefined">
      <q-markup-table v-for="host in siteSwitches" :key="host.nodeid" class="q-my-md">
        <thead>
          <tr>
            <td>
              {{ host.hostname }}
            </td>
            <td>
              Interface
            </td>
            <td>
              Status
            </td>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(data, inf) in host.result" :key="inf">
            <td></td>
            <td>
              {{ inf }}
            </td>
            <td>
              {{ data }}
            </td>
          </tr>
        </tbody>
      </q-markup-table>
    </div>
  </q-page>
</template>

<script>
import { ref, watch, computed } from 'vue'
import { api } from 'boot/axios'
import { useStore } from 'vuex'

export default {
  name: 'SiteActivation',

  setup () {
    const $store = useStore()
    const site = ref(null)
    const sites = ref([])

    watch(site, () => {
      $store.dispatch('tasks/getSiteStatus', site.value)
    })

    const siteSwitches = computed(() => {
      return $store.state.tasks.taskResult.results
    })

    const btnDisabled = computed(() => {
      if (siteSwitches.value !== undefined) {
        return false
      } else {
        return true
      }
    })

    const btnLabel = computed(() => {
      if (siteSwitches.value !== undefined) {
        if (Object.values($store.state.tasks.taskResult.results[0].result)[0] !== 'up') {
          return 'activate'
        }
      }
      return 'deactivate'
    })

    const runTask = () => {
      $store.dispatch('tasks/activateDeactivateSite', { action: btnLabel, site })
    }

    api.get('/tasks/network/activate_site')
      .then(response => {
        sites.value = response.data.sites
      })

    return { site, sites, siteSwitches, btnDisabled, btnLabel, runTask }
  }
}
</script>
