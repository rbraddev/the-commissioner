import { LocalStorage } from 'quasar'
import { api } from 'boot/axios'

export function SET_USER_DATA (state, userData) {
  LocalStorage.set('user', userData)
  state.user = userData
}

export function SET_ACCESS_TOKEN (state, accessToken) {
  LocalStorage.set('accessToken', accessToken)
  api.defaults.headers.common.Authorization = `Bearer ${
    accessToken
  }`
  state.accessToken = accessToken
}

export function LOGOUT () {
  LocalStorage.remove('user')
  LocalStorage.remove('accessToken')
  location.reload()
}

export function SET_SESSION_TIMEOUT (state, updatedSessionTimeout) {
  state.sessionTimeout = updatedSessionTimeout
}
