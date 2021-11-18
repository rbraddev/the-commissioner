<template>
  <div>
    <q-card>
        <q-card-section>
          <div v-if="isDialog" class="q-mb-sm text-center text-negative">Your session has expired, please login again</div>
          <q-form @keydown.enter.prevent="loginButton">
            <q-input filled v-model="username" label="username" class="q-mb-md" />
            <q-input filled v-model="password" label="password" type="password" class="q-mb-md" />
            <q-btn label="login" @click="loginButton" class="full-width" color="primary" />
          </q-form>
        </q-card-section>
      </q-card>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

export default {
  name: 'Login',
  props: ['isDialog'],

  setup (props) {
    const $store = useStore()
    const $router = useRouter()
    const username = ref('')
    const password = ref('')

    const loginButton = () => {
      $store
        .dispatch('auth/login', {
          username: username.value,
          password: password.value
        })
        .then(() => {
          if (props.isDialog) {
            $store.dispatch('auth/setTimeout', false)
          } else {
            $router.push({ name: 'dashboard' })
          }
        })
        .catch((error) => { console.log(error) })
    }

    return { username, password, loginButton }
  }
}
</script>
