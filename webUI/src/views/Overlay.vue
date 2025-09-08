<template>
  <div class="overlay-container">
    <div class="results-list">
      <div 
        v-for="(item, index) in allResults" 
        :key="item.id"
        class="result-card"
        :class="{ 'mic-result': item.type === 'mic', 'cap-result': item.type === 'cap', 'fade-in': index === 0 }"
        draggable="true"
        @dragstart="handleDragStart(index)"
        @dragover="handleDragOver"
        @drop="handleDrop(index)"
      >
        <div class="result-content">
          <div class="source-tag" :class="item.type">
            {{ item.type === 'mic' ? '麦克风' : '桌面音频' }}
          </div>
          <div class="result-text">{{ item.text }}</div>
        </div>
      </div>
      
      <div v-if="allResults.length === 0" class="empty-state">
        等待识别结果...
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
    allResults() {
      return this.$store.getters.allResults
    }
  },
  data() {
    return {
      socket: null,
      draggedIndex: null
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
    
    handleDragStart(index) {
      this.draggedIndex = index
    },
    
    handleDragOver(e) {
      e.preventDefault()
    },
    
    handleDrop(targetIndex) {
      if (this.draggedIndex === null || this.draggedIndex === targetIndex) return
      
      const results = [...this.allResults]
      const draggedItem = results[this.draggedIndex]
      
      // 移除拖拽的项目
      results.splice(this.draggedIndex, 1)
      
      // 插入到目标位置
      results.splice(targetIndex, 0, draggedItem)
      
      // 更新store中的数据
      const micResults = results.filter(r => r.type === 'mic').map(r => r.text)
      const capResults = results.filter(r => r.type === 'cap').map(r => r.text)
      
      this.$store.commit('SET_MIC_RESULTS', micResults)
      this.$store.commit('SET_CAP_RESULTS', capResults)
      
      this.draggedIndex = null
    }
  }
}
</script>

<style scoped>
.overlay-container {
  width: 100%;
  height: 100%;
  background: rgba(128, 128, 128, 0.05);
  user-select: none;
  position: relative;
  border: none;
  border-radius: 8px;
  box-sizing: border-box;
  backdrop-filter: blur(2px);
}

.results-list {
  width: 100%;
  height: 100%;
  padding: 10px;
  box-sizing: border-box;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.result-card {
  background: rgba(0, 0, 0, 0.15);
  border-radius: 6px;
  padding: 8px 12px;
  cursor: move;
  transition: all 0.3s ease;
  margin-bottom: 6px;
  backdrop-filter: blur(1px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  position: relative;
}

.result-card:hover {
  background: rgba(0, 0, 0, 0.3);
  transform: translateY(-1px);
}

.result-content {
  display: flex;
  align-items: flex-start;
  gap: 8px;
}

.source-tag {
  font-size: 11px;
  font-weight: bold;
  padding: 2px 6px;
  border-radius: 3px;
  color: #000;
  white-space: nowrap;
  flex-shrink: 0;
  margin-top: 1px;
}

.source-tag.mic {
  background: #00ff88;
}

.source-tag.cap {
  background: #ff6b35;
}

.result-text {
  font-size: 14px;
  line-height: 1.4;
  color: rgba(255, 255, 255, 0.95);
  word-break: break-word;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.8);
  flex: 1;
}

.empty-state {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: rgba(255, 255, 255, 0.5);
  font-style: italic;
  font-size: 14px;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.8);
}

.fade-in {
  animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.result-card[draggable="true"] {
  cursor: grab;
}

.result-card[draggable="true"]:active {
  cursor: grabbing;
}

/* 半透明滚动条样式 */
.results-list::-webkit-scrollbar {
  width: 6px;
}

.results-list::-webkit-scrollbar-track {
  background: rgba(128, 128, 128, 0.1);
  border-radius: 3px;
}

.results-list::-webkit-scrollbar-thumb {
  background: rgba(128, 128, 128, 0.3);
  border-radius: 3px;
}

.results-list::-webkit-scrollbar-thumb:hover {
  background: rgba(128, 128, 128, 0.5);
}

/* Firefox滚动条 */
.results-list {
  scrollbar-width: thin;
  scrollbar-color: rgba(128, 128, 128, 0.3) rgba(128, 128, 128, 0.1);
}
body {
            background-color: transparent !important; /* 重要，以覆盖可能的父容器背景 */
        }
</style>