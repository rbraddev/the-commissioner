export function SET_INVENTORY_DATA (state, payload) {
  state.network = payload.network_devices
  state.desktop = payload.desktops
  state.interfaces = payload.interfaces
}

export function UPDATE_NETWORK (state, payload) {
  const stateNetworkIndex = state.network.findIndex(x => x.id === payload.id)
  state.network[stateNetworkIndex] = payload
}
