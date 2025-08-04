<template>
  <div class="overlay-container">
    <div class="recognition-panel">
      <div class="mic-section">
        <div class="section-header">
          <div class="icon mic-icon"></div>
          <span>麦克风</span>
        </div>
        <div class="results">
          <div 
            v-for="(text, index) in micResults" 
            :key="`mic-${index}`"
            class="result-item"
            :class="{ 'fade-in': index === 0 }"
          >
            {{ text }}
          </div>
          <div 
            v-for="i in (3 - micResults.length)" 
            :key="`mic-empty-${i}`"
            class="result-item empty"
          >
            等待识别...
          </div>
        </div>
      </div>

      <div class="cap-section">
        <div class="section-header">
          <div class="icon cap-icon"></div>
          <span>桌面音频</span>
        </div>
        <div class="results">
          <div 
            v-for="(text, index) in capResults" 
            :key="`cap-${index}`"
            class="result-item"
            :class="{ 'fade-in': index === 0 }"
          >
            {{ text }}
          </div>
          <div 
            v-for="i in (3 - capResults.length)" 
            :key="`cap-empty-${i}`"
            class="result-item empty"
          >
            等待识别...
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { io } from 'socket.io-client'

export default {
  name: 'Overlay',
  data() {
    return {
      socket: null
    }
  },
  computed: {
    micResults() {
      return this.$store.getters.micResults
    },
    capResults() {
      return this.$store.getters.capResults
    }
  },
  mounted() {
    // 创建socket连接
    this.socket = io()
    
    // 监听socket消息
    this.socket.on('mic', (data) => {
      this.$store.dispatch('addMicResult', data.text)
    })
    
    this.socket.on('cap', (data) => {
      this.$store.dispatch('addCapResult', data.text)
    })
    
    // 连接状态监听
    this.socket.on('connect', () => {
      console.log('Overlay socket connected')
    })
    
    this.socket.on('disconnect', () => {
      console.log('Overlay socket disconnected')
    })
  },
  beforeUnmount() {
    if (this.socket) {
      this.socket.off('mic')
      this.socket.off('cap')
      this.socket.off('connect')
      this.socket.off('disconnect')
      this.socket.disconnect()
    }
  }
}
</script>

<style scoped>
.overlay-container {
  width: 100vw;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  user-select: none;
}

.recognition-panel {
  display: flex;
  gap: 10px;
  padding: 10px;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 8px;
  backdrop-filter: blur(5px);
}

.mic-section, .cap-section {
  flex: 1;
  min-width: 180px;
  background: rgba(0, 0, 0, 0.4);
  border-radius: 8px;
  padding: 12px;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
  font-size: 12px;
  font-weight: bold;
  color: #00ff88;
}

.icon {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.mic-icon {
  background: #00ff88;
}

.cap-icon {
  background: #ff6b35;
}

.results {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.result-item {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  padding: 8px 10px;
  font-size: 11px;
  line-height: 1.3;
  color: rgba(255, 255, 255, 0.9);
  transition: all 0.3s ease;
  border-left: 2px solid transparent;
  max-height: 40px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.result-item:hover {
  background: rgba(255, 255, 255, 0.2);
  border-left-color: #00ff88;
}

.result-item.empty {
  color: rgba(255, 255, 255, 0.5);
  font-style: italic;
  text-align: center;
}

.fade-in {
  animation: fadeIn 0.5s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>