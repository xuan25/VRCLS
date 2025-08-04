import { createRouter, createWebHashHistory } from 'vue-router'
import Overlay from '../views/Overlay.vue'
import configPage from '../components/config-page.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: configPage
  },
  {
    path: '/overlay',
    name: 'Overlay',
    component: Overlay,
    meta: {
      transparent: true,
      frameless: true
    }
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router