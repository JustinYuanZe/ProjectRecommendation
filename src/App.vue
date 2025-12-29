<template>
  <v-app>
    <!-- Top Banner Bar -->
    <div class="top-banner">
      <v-container fluid class="px-6">
        <v-row align="center" no-gutters>
          <v-col cols="auto">
            <span class="text-caption text-white">{{ $t('common.ministry') }}</span>
          </v-col>
        </v-row>
      </v-container>
    </div>

    <!-- Main Navigation Header -->
    <v-app-bar color="white" class="main-header" elevation="1" height="56">
      <v-container fluid class="px-4">
        <v-row align="center" no-gutters>
          <v-col cols="auto" class="d-flex align-center">
            <div class="logo-section" @click="$router.push({ name: 'Home' })" style="cursor: pointer;">
              <img :src="logo" alt="Advisory System logo" height="36" width="36" class="mr-3" />
              <div class="logo-text">
                <div class="text-subtitle-1 font-weight-bold blue-primary--text">{{ $t('common.appName') }}</div>
              </div>
            </div>
          </v-col>

          <v-spacer></v-spacer>

          <v-col cols="auto">
            <div class="nav-menu d-flex align-center">
              <v-btn v-for="item in menuItems" :key="item.key" :to="item.to" variant="text" class="nav-btn mx-1"
                size="small">
                {{ $t(item.labelKey) }}
              </v-btn>

              <!-- Language Switcher -->
              <v-menu>
                <template v-slot:activator="{ props }">
                  <v-btn v-bind="props" variant="text" class="nav-btn mx-1" size="small">
                    <v-icon size="small" class="mr-1">mdi-earth</v-icon>
                    {{ currentLocaleName }}
                    <v-icon size="x-small" class="ml-1">mdi-chevron-down</v-icon>
                  </v-btn>
                </template>
                <v-list density="compact">
                  <v-list-item
                    v-for="lang in availableLocales"
                    :key="lang.code"
                    @click="changeLanguage(lang.code)"
                    :active="currentLocale === lang.code"
                  >
                    <template v-slot:prepend>
                      <v-icon v-if="currentLocale === lang.code" color="primary" size="small">mdi-check</v-icon>
                      <v-icon v-else size="small"></v-icon>
                    </template>
                    <v-list-item-title>{{ lang.name }}</v-list-item-title>
                  </v-list-item>
                </v-list>
              </v-menu>

              <!-- Auth buttons -->
              <template v-if="!auth.isLoggedIn">
                <v-btn :to="{ name: 'Login' }" variant="outlined" color="primary" size="small" class="mx-1">
                  {{ $t('nav.login') }}
                </v-btn>
                <v-btn :to="{ name: 'Register' }" color="primary" size="small" class="mx-1">
                  {{ $t('nav.register') }}
                </v-btn>
              </template>
              <template v-else>
                <v-menu>
                  <template v-slot:activator="{ props }">
                    <v-btn v-bind="props" variant="text" class="nav-btn mx-1" size="small">
                      <v-icon size="small" class="mr-1">mdi-account-circle</v-icon>
                      {{ auth.user.username }}
                    </v-btn>
                  </template>
                  <v-list>
                    <v-list-item :to="{ name: 'Profile' }">
                      <v-list-item-title>{{ $t('nav.profile') }}</v-list-item-title>
                    </v-list-item>
                    <v-list-item @click="handleLogout">
                      <v-list-item-title>{{ $t('nav.logout') }}</v-list-item-title>
                    </v-list-item>
                  </v-list>
                </v-menu>
              </template>
            </div>
          </v-col>
        </v-row>
      </v-container>
    </v-app-bar>

    <!-- Main Content -->
    <v-main class="main-content">
      <!-- Listen to events emitted by routed components (e.g. show-snackbar) -->
      <router-view @show-snackbar="showSnackbar"></router-view>
    </v-main>

    <v-footer v-if="$route.name === 'Home'" class="main-footer" color="white">
      <v-container fluid class="px-4 py-3">
        <v-row dense>
          <v-col cols="12" md="4">
            <div class="footer-logo mb-2">
              <img :src="logo" alt="Advisory System logo" height="28" width="28" class="mb-1" />
              <div class="text-body-2 font-weight-bold">{{ $t('common.appName') }}</div>
            </div>
          </v-col>

          <v-col cols="6" md="4">
            <div class="footer-section">
              <h4 class="text-body-2 font-weight-bold mb-2">{{ $t('footer.aboutPlatform') }}</h4>
              <div class="footer-links">
                <router-link to="/about" class="footer-link">{{ $t('nav.about') }}</router-link>
                <router-link to="/faq" class="footer-link">{{ $t('nav.faq') }}</router-link>
              </div>
            </div>
          </v-col>

          <v-col cols="6" md="4">
            <div class="footer-section">
              <h4 class="text-body-2 font-weight-bold mb-2">{{ $t('footer.services') }}</h4>
              <div class="footer-links">
                <router-link to="/career-test" class="footer-link">{{ $t('footer.skillsAssessment') }}</router-link>
                <router-link to="/results" class="footer-link">{{ $t('footer.learningRecommendations') }}</router-link>
              </div>
            </div>
          </v-col>
        </v-row>

        <v-divider class="my-2"></v-divider>

        <v-row align="center">
          <v-col cols="12" class="text-center py-1">
            <div class="text-caption text--secondary">
              {{ $t('common.copyright') }}
            </div>
          </v-col>
        </v-row>
      </v-container>
    </v-footer>

    <!-- Snackbar for notifications -->
    <v-snackbar v-model="snackbar.show" :color="snackbar.color" :timeout="snackbar.timeout" location="bottom">
      {{ snackbar.text }}
      <template v-slot:actions>
        <v-btn variant="text" @click="snackbar.show = false">
          {{ $t('common.close') }}
        </v-btn>
      </template>
    </v-snackbar>

    <!-- Chatbot Component -->
    <Chatbot />
  </v-app>
</template>

<script>
import { auth } from './store/auth'
import Chatbot from './components/Chatbot.vue'
import { setLocale, getLocale } from './i18n'

export default {
  components: {
    Chatbot
  },
  name: 'App',
  data() {
    return {
      // public assets are served at root path — use /logo.png
      logo: '/logo.png',
      auth,
      menuItems: [
        { key: 'home', labelKey: 'nav.home', to: { name: 'Home' } },
        { key: 'careerTest', labelKey: 'nav.careerTest', to: { name: 'CareerTest' } },
        { key: 'results', labelKey: 'nav.results', to: { name: 'Results' } }
      ],
      snackbar: {
        show: false,
        text: '',
        color: 'info',
        timeout: 4000
      },
      availableLocales: [
        { code: 'en', name: 'English' },
        { code: 'zh-TW', name: '繁體中文' }
      ]
    }
  },
  computed: {
    currentLocale() {
      return getLocale()
    },
    currentLocaleName() {
      const locale = this.availableLocales.find(l => l.code === this.currentLocale)
      return locale ? locale.name : 'English'
    }
  },
  methods: {
    showSnackbar(message, color = 'info') {
      this.snackbar.text = message
      this.snackbar.color = color
      this.snackbar.show = true
    },
    handleLogout() {
      auth.logout()
      this.$router.push({ name: 'Home' })
      this.showSnackbar(this.$t('auth.logoutSuccess'), 'success')
    },
    changeLanguage(locale) {
      setLocale(locale)
      // Force re-render by updating a key or using forceUpdate
      this.$forceUpdate()
    }
  }
}
</script>

<style>
.v-application {
  font-family: 'Microsoft JhengHei', 'PingFang TC', 'Helvetica Neue', Arial, sans-serif;
}

/* Top banner styles */
.top-banner {
  background: linear-gradient(135deg, #1565C0 0%, #0D47A1 100%);
  min-height: 24px;
  display: flex;
  align-items: center;
  padding: 2px 0;
}

/* Main header styles */
.main-header {
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
}

.logo-section {
  display: flex;
  align-items: center;
}

.logo-text .text-h5 {
  line-height: 1;
  color: #1565C0 !important;
}

.nav-menu .nav-btn {
  font-weight: 500;
  letter-spacing: 0.5px;
  color: #37474F !important;
  text-transform: none;
}

.nav-menu .nav-btn:hover {
  background-color: rgba(21, 101, 192, 0.08);
  color: #1565C0 !important;
}

/* Main content styles */
.main-content {
  min-height: calc(100vh - 200px);
  background-color: #FAFAFA;
}

/* Footer styles */
.main-footer {
  background: #ffffff;
  border-top: 1px solid rgba(0, 0, 0, 0.08);
  padding: 12px 0 8px 0;
}

.footer-logo {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.footer-section h4 {
  color: #212121;
  border-bottom: 1px solid #1565C0;
  padding-bottom: 4px;
  margin-bottom: 8px;
}

.footer-links {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.footer-link {
  color: #666;
  text-decoration: none;
  font-size: 12px;
  transition: color 0.3s ease;
}

.footer-link:hover {
  color: #1565C0;
  text-decoration: none;
}

/* Utility classes */
.blue-primary--text {
  color: #1565C0 !important;
}

.text--secondary {
  color: #757575 !important;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .nav-menu {
    display: none;
  }

  .footer-section {
    margin-bottom: 12px;
  }

  .main-header {
    height: 48px !important;
  }

  .logo-text .text-subtitle-1 {
    font-size: 0.9rem !important;
  }
}
</style>
