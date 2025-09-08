import { createStore } from 'vuex'

export default createStore({
  state: {
    overlay: {
      micResults: [],
      capResults: [],
      allResults: []
    }
  },
  mutations: {
    addMicResult(state, text) {
      state.overlay.allResults.unshift({
        text: text,
        type: 'mic',
        time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit', second: '2-digit' })
      })
      if (state.overlay.allResults.length > 20) {
        state.overlay.allResults = state.overlay.allResults.slice(0, 20)
      }
    },
    addCapResult(state, text) {
      state.overlay.allResults.unshift({
        text: text,
        type: 'cap',
        time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit', second: '2-digit' })
      })
      if (state.overlay.allResults.length > 20) {
        state.overlay.allResults = state.overlay.allResults.slice(0, 20)
      }
    },
    clearMicResults(state) {
      state.overlay.micResults = []
    },
    clearCapResults(state) {
      state.overlay.capResults = []
    },
    SET_MIC_RESULTS(state, results) {
      state.overlay.micResults = results
    },
    SET_CAP_RESULTS(state, results) {
      state.overlay.capResults = results
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
    capResults: state => state.overlay.capResults,
    allResults: state => state.overlay.allResults
  }
})