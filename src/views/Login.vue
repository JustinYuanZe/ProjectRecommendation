<template>
  <v-container class="fill-height">
    <v-row justify="center" align="center">
      <v-col cols="12" sm="8" md="4">
        <v-card class="elevation-12">
          <v-toolbar color="primary" dark flat>
            <v-toolbar-title>Login</v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-form @submit.prevent="handleLogin">
              <v-text-field v-model="username" label="Username" prepend-icon="mdi-account" type="text"
                required></v-text-field>
              <v-text-field v-model="password" label="Password" prepend-icon="mdi-lock" type="password"
                required></v-text-field>
              <div class="text-center mt-3">
                <v-btn color="primary" type="submit" :loading="loading">Login</v-btn>
              </div>
            </v-form>
            <div class="text-center mt-4">
              <router-link to="/register">Don't have an account? Register</router-link>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-snackbar v-model="snackbar.show" :color="snackbar.color">
      {{ snackbar.text }}
      <template v-slot:actions>
        <v-btn variant="text" @click="snackbar.show = false">Close</v-btn>
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
      loading: false,
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
