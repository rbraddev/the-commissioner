export function SET_TASK_ID (state, payload) {
  state.taskId = payload
  state.taskResult = {}
}

export function SET_TASK_RESULT (state, payload) {
  state.taskResult = payload
}
