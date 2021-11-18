<template>
  <q-layout view="hHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="toggleLeftDrawer"
        />

        <q-toolbar-title>
          The Commissioner
        </q-toolbar-title>
        <LogoutBtn />
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
    >
      <q-list>
        <q-item-label
          header
        >
          Inventory
        </q-item-label>

        <DrawLink
          v-for="link in inventoryLinks"
          :key="link.title"
          v-bind="link"
        />
      </q-list>
      <q-list>
        <q-item-label
          header
        >
          Tasks
        </q-item-label>

        <DrawLink
          v-for="link in taskLinks"
          :key="link.title"
          v-bind="link"
        />
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
    <q-dialog v-model="showDialog" seamless position="bottom">
      <div>
        TEST DIALOG
      </div>
    </q-dialog>
  </q-layout>
</template>

<script>
import DrawLink from 'components/DrawLink'
import LogoutBtn from 'components/LogoutBtn'
import { useStore } from 'vuex'
import { api } from 'boot/axios'
import { useQuasar } from 'quasar'

const inventoryList = [
  {
    title: 'Search',
    caption: 'Search Inventory',
    icon: 'search',
    link: '/dashboard/search',
    access_lvl: 1
  }
]

const taskList = [
  {
    title: 'Site Activation/Deactivation',
    caption: 'Activate/Deactivate Site',
    icon: 'school',
    link: '/dashboard/tasks/site_activation',
    access_lvl: 2
  }
]

import { defineComponent, ref } from 'vue'

export default defineComponent({
  name: 'MainLayout',

  components: {
    DrawLink,
    LogoutBtn
  },

  setup () {
    const $q = useQuasar()
    const $store = useStore()
    const leftDrawerOpen = ref(false)

    const user = $q.localStorage.getItem('user')

    const inventoryLinks = inventoryList.filter(item => item.access_lvl <= user.access_lvl)

    const taskLinks = taskList.filter(i => i.access_lvl < user.access_lvl)

    api.interceptors.response.use(
      response => response,
      error => {
        if (error.response.status === 401) {
          $store.dispatch('auth/setTimeout', true)
        }
      }
    )

    return {
      showDialog: true,
      inventoryLinks,
      taskLinks,
      leftDrawerOpen,
      toggleLeftDrawer () {
        leftDrawerOpen.value = !leftDrawerOpen.value
      }
    }
  }
})
</script>
