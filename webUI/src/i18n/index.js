import { createI18n } from 'vue-i18n'
import zh from './locales/zh.js'
import en from './locales/en.js'
import ja from './locales/ja.js'

const messages = {
  zh,
  en,
  ja
}

// 获取浏览器语言或默认使用中文
const getDefaultLocale = () => {
  const savedLocale = localStorage.getItem('locale')
  if (savedLocale && messages[savedLocale]) {
    return savedLocale
  }
  
  const browserLocale = navigator.language.toLowerCase()
  if (browserLocale.startsWith('ja')) {
    return 'ja'
  } else if (browserLocale.startsWith('en')) {
    return 'en'
  }
  return 'zh'
}

const i18n = createI18n({
  legacy: false, // 使用 Composition API 模式
  locale: getDefaultLocale(),
  fallbackLocale: 'zh',
  messages
})

export default i18n 