<template>
  <q-page class="flex flex-center">
    <div class="full-width" style="max-width: 350px;">
      <h5 class="q-my-md text-center">
        Login
      </h5>
      <Login isModel="false" />
    </div>
  </q-page>
</template>

<script>
import { defineComponent } from 'vue'
import Login from 'components/Login'

export default defineComponent({
  name: 'PageIndex',
  components: { Login }
})
</script>
