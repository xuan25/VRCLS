<template>
  <div id="app-container">
    <!-- 拖拽区域 -->
    <div id="drag-region" @mousedown="handleMouseDown"></div>
    
    <!-- 主要内容 -->
    <router-view />
    
    <!-- 调整大小手柄 -->
    <div id="resize-handle-top" class="resize-handle" @mousedown="handleMouseDown"></div>
    <div id="resize-handle-right" class="resize-handle" @mousedown="handleMouseDown"></div>
    <div id="resize-handle-bottom" class="resize-handle" @mousedown="handleMouseDown"></div>
    <div id="resize-handle-left" class="resize-handle" @mousedown="handleMouseDown"></div>
    <div id="resize-handle-top-left" class="resize-handle" @mousedown="handleMouseDown"></div>
    <div id="resize-handle-top-right" class="resize-handle" @mousedown="handleMouseDown"></div>
    <div id="resize-handle-bottom-left" class="resize-handle" @mousedown="handleMouseDown"></div>
    <div id="resize-handle-bottom-right" class="resize-handle" @mousedown="handleMouseDown"></div>
  </div>
</template>

<script>
import configPage from './components/config-page.vue'

export default {
  name: 'App',
  components: {
    configPage
  },
  data() {
    return {
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
    window.addEventListener('mousemove', this.handleMouseMove)
    window.addEventListener('mouseup', this.handleMouseUp)
  },
  beforeUnmount() {
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

<style>
#app-container {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

#drag-region {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 30px;
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

html, body, #app {
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
  