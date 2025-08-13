<template>
  <div class="overlay-container">
    <!-- 拖拽区域 -->
    <div id="drag-region" class="drag-region" @mousedown="handleMouseDown"></div>
    
    <!-- 调整大小手柄 -->
    <div id="resize-handle-top" class="resize-handle" @mousedown="handleMouseDown"></div>
    <div id="resize-handle-right" class="resize-handle" @mousedown="handleMouseDown"></div>
    <div id="resize-handle-bottom" class="resize-handle" @mousedown="handleMouseDown"></div>
    <div id="resize-handle-left" class="resize-handle" @mousedown="handleMouseDown"></div>
    <div id="resize-handle-top-left" class="resize-handle" @mousedown="handleMouseDown"></div>
    <div id="resize-handle-top-right" class="resize-handle" @mousedown="handleMouseDown"></div>
    <div id="resize-handle-bottom-left" class="resize-handle" @mousedown="handleMouseDown"></div>
    <div id="resize-handle-bottom-right" class="resize-handle" @mousedown="handleMouseDown"></div>
    
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
  data() {
    return {
      socket: null,
      isInteracting: false,
      interactionType: '',
      handleId: '',
      startState: {
        windowX: 0,
        windowY: 0,
        windowWidth: 0,
        windowHeight: 0,
        mouseX: 0,
        mouseY: 0
      }
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
    
    // 添加拖拽和调整大小的事件监听
    window.addEventListener('mousemove', this.handleMouseMove)
    window.addEventListener('mouseup', this.handleMouseUp)
  },
  beforeUnmount() {
    if (this.socket) {
      this.socket.off('mic')
      this.socket.off('cap')
      this.socket.off('connect')
      this.socket.off('disconnect')
      this.socket.disconnect()
    }
    
    // 移除事件监听
    window.removeEventListener('mousemove', this.handleMouseMove)
    window.removeEventListener('mouseup', this.handleMouseUp)
  },
  methods: {
    async handleMouseDown(e) {
      if (!window.pywebview || !window.pywebview.api) {
        console.error("pywebview API is not available.")
        return
      }

      e.preventDefault()
      this.isInteracting = true
      this.handleId = e.target.id
      this.interactionType = this.handleId === 'drag-region' ? 'drag' : 'resize'
      
      const initialState = await window.pywebview.api.get_window_state()
      if (!initialState) return

      this.startState = {
        windowX: initialState.x,
        windowY: initialState.y,
        windowWidth: initialState.width,
        windowHeight: initialState.height,
        mouseX: e.screenX,
        mouseY: e.screenY
      }
    },
    
    handleMouseMove(e) {
      if (!this.isInteracting) return

      const deltaX = e.screenX - this.startState.mouseX
      const deltaY = e.screenY - this.startState.mouseY

      if (this.interactionType === 'drag') {
        const newX = this.startState.windowX + deltaX
        const newY = this.startState.windowY + deltaY
        window.pywebview.api.move(newX, newY)
      } else if (this.interactionType === 'resize') {
        let newWidth = this.startState.windowWidth
        let newHeight = this.startState.windowHeight

        if (this.handleId.includes('right')) {
          newWidth = this.startState.windowWidth + deltaX
        }
        if (this.handleId.includes('left')) {
          newWidth = this.startState.windowWidth - deltaX
          const newX = this.startState.windowX + deltaX
          window.pywebview.api.move(newX, this.startState.windowY)
        }
        if (this.handleId.includes('bottom')) {
          newHeight = this.startState.windowHeight + deltaY
        }
        if (this.handleId.includes('top')) {
          newHeight = this.startState.windowHeight - deltaY
          const newY = this.startState.windowY + deltaY
          window.pywebview.api.move(this.startState.windowX, newY)
        }
        
        window.pywebview.api.resize(Math.max(200, newWidth), Math.max(150, newHeight))
      }
    },
    
    handleMouseUp() {
      this.isInteracting = false
      this.interactionType = ''
      this.handleId = ''
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
  position: relative;
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

.drag-region {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 20px;
  z-index: 1000;
  cursor: move;
}

.resize-handle {
  position: fixed;
  z-index: 1001;
}

#resize-handle-top {
  top: 0;
  left: 5px;
  right: 5px;
  height: 5px;
  cursor: ns-resize;
}

#resize-handle-bottom {
  bottom: 0;
  left: 5px;
  right: 5px;
  height: 5px;
  cursor: ns-resize;
}

#resize-handle-left {
  left: 0;
  top: 5px;
  bottom: 5px;
  width: 5px;
  cursor: ew-resize;
}

#resize-handle-right {
  right: 0;
  top: 5px;
  bottom: 5px;
  width: 5px;
  cursor: ew-resize;
}

#resize-handle-top-left {
  top: 0;
  left: 0;
  width: 10px;
  height: 10px;
  cursor: nwse-resize;
}

#resize-handle-top-right {
  top: 0;
  right: 0;
  width: 10px;
  height: 10px;
  cursor: nesw-resize;
}

#resize-handle-bottom-left {
  bottom: 0;
  left: 0;
  width: 10px;
  height: 10px;
  cursor: nesw-resize;
}

#resize-handle-bottom-right {
  bottom: 0;
  right: 0;
  width: 10px;
  height: 10px;
  cursor: nwse-resize;
}
</style>