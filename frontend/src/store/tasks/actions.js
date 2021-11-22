import { api } from 'boot/axios'
import { config } from 'boot/config'

export function getSiteStatus ({ commit }, site) {
  return api.get(`/tasks/network/site_status/${site}`)
    .then((response) => {
      commit('SET_TASK_ID', response.data.task_id)
      const ws = new WebSocket(`${config.WS_URL}/${response.data.task_id}`)
      ws.onmessage = (event) => {
        const taskData = JSON.parse(JSON.parse(event.data))

        if (taskData.task_data.status === 'complete') {
          commit('SET_TASK_RESULT', taskData)
        }
      }
    })
}

export function activateDeactivateSite ({ dispatch }, { action, site }) {
  return api.post(`/tasks/network/${action.value}_site`, { site: site.value })
    .then((response) => {
      const ws = new WebSocket(`${config.WS_URL}/${response.data.task_id}`)
      ws.onmessage = (event) => {
        const taskData = JSON.parse(JSON.parse(event.data))

        if (taskData.task_data.status === 'complete') {
          dispatch('getSiteStatus', site.value)
        }
      }
    })
}
