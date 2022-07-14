import { boot } from 'quasar/wrappers'

const config = {
  WS_URL: 'wss://localhost/api/v1/tasks/ws'
}

export default boot(({ app }) => {
  app.config.globalProperties.$config = config
})

export { config }
