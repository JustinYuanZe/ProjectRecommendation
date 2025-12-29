import { createI18n } from 'vue-i18n'
import en from './locales/en'
import zhTW from './locales/zh-TW'

// Get saved language or detect from browser
function getDefaultLocale() {
  const saved = localStorage.getItem('locale')
  if (saved) return saved
  
  const browserLang = navigator.language || navigator.userLanguage
  if (browserLang.startsWith('zh')) {
    return 'zh-TW'
  }
  return 'en'
}

const i18n = createI18n({
  legacy: false, // Use Composition API mode
  locale: getDefaultLocale(),
  fallbackLocale: 'en',
  messages: {
    en,
    'zh-TW': zhTW
  }
})

export default i18n

// Helper to change language
export function setLocale(locale) {
  i18n.global.locale.value = locale
  localStorage.setItem('locale', locale)
  document.querySelector('html').setAttribute('lang', locale)
}

// Helper to get current locale
export function getLocale() {
  return i18n.global.locale.value
}
