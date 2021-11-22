import { boot } from 'quasar/wrappers'

const config = {
  WS_URL: 'wss://api.networkdev.co.uk/tasks/ws'
}

export default boot(({ app }) => {
  app.config.globalProperties.$config = config
})

export { config }
