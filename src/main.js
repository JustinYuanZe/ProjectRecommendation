import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import i18n from './i18n'

// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import '@mdi/font/css/materialdesignicons.css'

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        colors: {
          primary: '#1565C0',          // UCAN's main blue
          secondary: '#37474F',        // Dark blue-gray
          accent: '#FF7043',           // Orange accent
          error: '#D32F2F',
          info: '#1976D2',
          success: '#388E3C',
          warning: '#F57C00',
          'ucan-blue': '#1565C0',      // Main UCAN blue
          'ucan-dark-blue': '#0D47A1', // Darker blue for gradients
          'ucan-light-blue': '#42A5F5', // Lighter blue for hover
          'ucan-orange': '#FF7043',    // UCAN orange accent
          'ucan-gray': '#37474F',      // Text gray
          'ucan-light-gray': '#ECEFF1', // Background gray
          'ucan-green': '#43A047',     // Success green
          'text-primary': '#212121',
          'text-secondary': '#757575',
          'background': '#FAFAFA',
          'surface': '#FFFFFF'
        },
      },
    },
  },
})

const app = createApp(App)

app.use(router)
app.use(vuetify)
app.use(i18n)

app.mount('#app')
