import { api } from 'boot/axios'

export function login ({ commit }, credentials) {
  return api.post('/auth/token', {}, {
    auth: {
      ...credentials
    }
  })
    .then(({ data }) => {
      commit('SET_USER_DATA', data.userdata)
      commit('SET_ACCESS_TOKEN', data.access_token)
    })
}

export function logout ({ commit }) {
  commit('LOGOUT')
}

export function setTimeout ({ commit }, updatedSessionTimeout) {
  commit('SET_SESSION_TIMEOUT', updatedSessionTimeout)
}
