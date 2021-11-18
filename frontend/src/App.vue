<template>
  <router-view />
  <q-dialog v-model="sessionTimeout">
    <div class="full-width" style="max-width: 350px;">
      <Login isDialog="true" />
    </div>
  </q-dialog>
</template>
<script>
import { defineComponent, computed } from 'vue'
import { useQuasar } from 'quasar'
import { useStore } from 'vuex'
import Login from 'components/Login.vue'

export default defineComponent({
  components: { Login },
  name: 'App',

  setup () {
    const $store = useStore()
    const $q = useQuasar()

    const sessionTimeout = computed(() => {
      return $store.state.auth.sessionTimeout
    })

    const user = $q.localStorage.getItem('user')
    const accessToken = $q.localStorage.getItem('accessToken')
    if (user) {
      $store.commit('auth/SET_USER_DATA', user)
    }
    if (accessToken) {
      $store.commit('auth/SET_ACCESS_TOKEN', accessToken)
    }
    return { sessionTimeout }
  }
})
</script>
