import { createStore } from 'vuex'

export default createStore({
  state: {
    overlay: {
      micResults: [],
      capResults: []
    }
  },
  mutations: {
    addMicResult(state, text) {
      state.overlay.micResults.unshift(text)
      if (state.overlay.micResults.length > 3) {
        state.overlay.micResults = state.overlay.micResults.slice(0, 3)
      }
    },
    addCapResult(state, text) {
      state.overlay.capResults.unshift(text)
      if (state.overlay.capResults.length > 3) {
        state.overlay.capResults = state.overlay.capResults.slice(0, 3)
      }
    },
    clearMicResults(state) {
      state.overlay.micResults = []
    },
    clearCapResults(state) {
      state.overlay.capResults = []
    }
  },
  actions: {
    addMicResult({ commit }, text) {
      commit('addMicResult', text)
    },
    addCapResult({ commit }, text) {
      commit('addCapResult', text)
    }
  },
  getters: {
    micResults: state => state.overlay.micResults,
    capResults: state => state.overlay.capResults
  }
})