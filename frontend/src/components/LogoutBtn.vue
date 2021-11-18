<template>
  <div>
    <q-btn
      flat
      dense
      round
      icon="logout"
      @click="logout"
    />
  </div>
</template>

<script>
import { useStore } from 'vuex'

export default {
  setup () {
    const $store = useStore()

    const logout = () => {
      $store.dispatch('auth/logout')
    }
    return { logout }
  }
}
</script>
