<template>
  <v-container class="login-container fill-height">
    <v-row justify="center" align="center" class="fill-height">
      <v-col cols="12" sm="10" md="5" lg="4" xl="3">
        <v-card elevation="8" class="login-card" rounded="lg">
          <!-- Header with gradient -->
          <div class="login-header">
            <v-icon size="64" color="white" class="mb-3">mdi-lock-open</v-icon>
            <h1 class="text-h5 font-weight-bold text-white mb-1">{{ $t('auth.loginTitle') }}</h1>
            <p class="text-body-2 text-white text-opacity-90">{{ $t('auth.loginSubtitle') }}</p>
          </div>

          <v-card-text class="pa-6">
            <v-form @submit.prevent="handleLogin">
              <v-text-field 
                v-model="username" 
                :label="$t('auth.username')" 
                prepend-inner-icon="mdi-account" 
                type="text"
                variant="outlined"
                color="primary"
                class="mb-3"
                required
                autofocus
                :error-messages="errors.username"
              ></v-text-field>

              <v-text-field 
                v-model="password" 
                :label="$t('auth.password')" 
                prepend-inner-icon="mdi-lock" 
                :type="showPassword ? 'text' : 'password'"
                :append-inner-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                @click:append-inner="showPassword = !showPassword"
                variant="outlined"
                color="primary"
                class="mb-4"
                required
                :error-messages="errors.password"
              ></v-text-field>

              <v-btn 
                color="primary" 
                type="submit" 
                :loading="loading" 
                block 
                size="large"
                class="mb-4 text-none font-weight-bold"
                elevation="2"
              >
                <v-icon start>mdi-login</v-icon>
                {{ loading ? $t('auth.loggingIn') : $t('auth.loginButton') }}
              </v-btn>

              <!-- Register Link -->
              <div class="text-center">
                <v-divider class="mb-3"></v-divider>
                <span class="text-body-2 text-grey-darken-1">{{ $t('auth.noAccount') }}</span>
                <router-link to="/register" class="ml-1 text-body-2 text-primary text-decoration-none font-weight-bold">
                  {{ $t('auth.registerNow') }}
                </router-link>
              </div>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Snackbar for notifications -->
    <v-snackbar 
      v-model="snackbar.show" 
      :color="snackbar.color"
      location="top"
      :timeout="3000"
    >
      <div class="d-flex align-center">
        <v-icon start>{{ snackbar.color === 'success' ? 'mdi-check-circle' : 'mdi-alert-circle' }}</v-icon>
        {{ snackbar.text }}
      </div>
      <template v-slot:actions>
        <v-btn variant="text" @click="snackbar.show = false">{{ $t('common.close') }}</v-btn>
      </template>
    </v-snackbar>
  </v-container>
</template>

<script>
import { auth } from '../store/auth'
import { API_URL } from '../config/api'

export default {
  name: 'Login',
  data() {
    return {
      username: '',
      password: '',
      showPassword: false,
      loading: false,
      errors: {
        username: '',
        password: ''
      },
      snackbar: {
        show: false,
        text: '',
        color: 'error'
      }
    }
  },
  methods: {
    async handleLogin() {
      this.loading = true
      try {
        const response = await fetch(`${API_URL}/login`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username: this.username, password: this.password })
        })
        const data = await response.json()

        if (data.success && data.accessToken && data.refreshToken) {
          auth.login(data.user, data.accessToken, data.refreshToken)
          this.showSnackbar(this.$t('auth.loginSuccess'), 'success')

          const redirectPath = sessionStorage.getItem('redirectAfterLogin')
          if (redirectPath) {
            sessionStorage.removeItem('redirectAfterLogin')
            this.$router.push(redirectPath)
          } else {
            this.$router.push({ name: 'Home' })
          }
        } else {
          this.showSnackbar(data.message || 'Login failed', 'error')
        }
      } catch (error) {
        this.showSnackbar('An error occurred', 'error')
      } finally {
        this.loading = false
      }
    },
    showSnackbar(text, color) {
      this.snackbar.text = text
      this.snackbar.color = color
      this.snackbar.show = true
    }
  }
}
</script>

<style scoped>
.login-container {
  min-height: calc(100vh - 64px);
  background-color: #f5f5f5;
}

.login-card {
  overflow: hidden;
}

.login-header {
  background: linear-gradient(135deg, #1976d2 0%, #1565c0 100%);
  padding: 48px 24px;
  text-align: center;
}

/* Smooth transitions */
.v-text-field {
  transition: all 0.3s ease;
}

.v-btn {
  transition: all 0.3s ease;
}

.v-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* Responsive adjustments */
@media (max-width: 600px) {
  .login-header {
    padding: 32px 16px;
  }
}
</style>
