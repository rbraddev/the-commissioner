import { api } from 'boot/axios'

export function search ({ commit }, searchString) {
  return api.get('/inventory/search', { params: { q: searchString } })
    .then((response) => {
      commit('SET_INVENTORY_DATA', response.data[0])
    })
}

export function getNetwork ({ commit }, nodeid) {
  return api.get('/inventory/network', { params: { nodeids: nodeid } })
    .then((response) => {
      commit('UPDATE_NETWORK', response.data[0])
    })
}
