<template>
  <div>
    <q-toolbar>
        <q-form
          @keydown.enter.prevent="searchClick"
          class="full-width"
        >
          <q-input
            dense
            placeholder="Search"
            borderless
            class="full-width"
            v-model="searchString"
          >
          <q-btn
            flat
            dense
            round
            icon="search"
            name="search"
            @click="searchClick"
          />
          </q-input>
        </q-form>
      </q-toolbar>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useStore } from 'vuex'

export default {
  name: 'SearchBar',
  setup () {
    const $store = useStore()
    const searchString = ref('')

    const searchClick = () => {
      $store.dispatch('inventory/search', searchString.value)
    }

    return { searchString, searchClick }
  }
}
</script>
