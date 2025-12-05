<template>
  <v-container class="fill-height">
    <v-row justify="center" align="center">
      <v-col cols="12" sm="8" md="6">
        <v-card class="elevation-12">
          <v-toolbar color="primary" dark flat>
            <v-toolbar-title>{{ $t('auth.registerTitle') }}</v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <p class="text-body-2 text-grey mb-4">{{ $t('auth.registerSubtitle') }}</p>
            <v-form ref="form" @submit.prevent="handleRegister" v-model="valid">
              <v-text-field 
                v-model="username" 
                :label="$t('auth.username')" 
                prepend-icon="mdi-account" 
                type="text"
                :rules="usernameRules"
                :counter="50"
                required></v-text-field>
              <v-text-field 
                v-model="password" 
                :label="$t('auth.password')" 
                prepend-icon="mdi-lock" 
                :type="showPassword ? 'text' : 'password'"
                :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                @click:append="showPassword = !showPassword"
                :rules="passwordRules"
                required></v-text-field>
              <v-text-field 
                v-model="confirmPassword" 
                :label="$t('auth.confirmPassword')" 
                prepend-icon="mdi-lock-check" 
                :type="showConfirmPassword ? 'text' : 'password'"
                :append-icon="showConfirmPassword ? 'mdi-eye' : 'mdi-eye-off'"
                @click:append="showConfirmPassword = !showConfirmPassword"
                :rules="confirmPasswordRules"
                required></v-text-field>
              <v-select 
                v-model="department" 
                :items="departments" 
                :label="$t('auth.department')" 
                prepend-icon="mdi-school"
                :rules="requiredRules"
                required></v-select>
              
              <v-radio-group v-model="identity" row>
                <template v-slot:label>
                  <span class="text-body-2">{{ $t('profile.identity') }}</span>
                </template>
                <v-radio :label="$t('profile.student')" value="student"></v-radio>
                <v-radio :label="$t('profile.unemployed')" value="Unemployed"></v-radio>
                <v-radio :label="$t('profile.employed')" value="employed"></v-radio>
              </v-radio-group>

              <v-radio-group v-model="gender" row>
                <template v-slot:label>
                  <span class="text-body-2">{{ $t('profile.gender') }}</span>
                </template>
                <v-radio :label="$t('profile.female')" value="female"></v-radio>
                <v-radio :label="$t('profile.male')" value="male"></v-radio>
              </v-radio-group>

              <v-text-field 
                v-model="email" 
                :label="$t('profile.email')" 
                prepend-icon="mdi-email"
                type="email"
                :rules="emailRules"></v-text-field>

              <div class="text-center mt-3">
                <v-btn color="primary" type="submit" :loading="loading" block size="large">
                  {{ loading ? $t('auth.registering') : $t('auth.registerButton') }}
                </v-btn>
              </div>
            </v-form>
            <div class="text-center mt-4">
              <span class="text-grey">{{ $t('auth.haveAccount') }}</span>
              <router-link to="/login" class="ml-1">{{ $t('auth.loginNow') }}</router-link>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-snackbar v-model="snackbar.show" :color="snackbar.color">
      {{ snackbar.text }}
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
  name: 'Register',
  data() {
    return {
      valid: false,
      username: '',
      password: '',
      confirmPassword: '',
      showPassword: false,
      showConfirmPassword: false,
      department: null,
      identity: 'student',
      gender: 'female',
      email: '',
      departments: [
        'Department of Computer Science and Engineering',
        'Department of Information Management',
        'Department of Information Communication',
        'International Bachelor Program in Informatics'
      ],
      loading: false,
      snackbar: {
        show: false,
        text: '',
        color: 'error'
      }
    }
  },
  computed: {
    usernameRules() {
      return [
        v => !!v || this.$t('auth.usernameRequired'),
        v => (v && v.length >= 3 && v.length <= 50) || this.$t('auth.usernameLength')
      ]
    },
    passwordRules() {
      return [
        v => !!v || this.$t('auth.passwordRequired'),
        v => (v && v.length >= 6) || this.$t('auth.passwordLength')
      ]
    },
    confirmPasswordRules() {
      return [
        v => !!v || this.$t('auth.passwordRequired'),
        v => v === this.password || this.$t('auth.passwordMatch')
      ]
    },
    requiredRules() {
      return [
        v => !!v || this.$t('auth.departmentRequired')
      ]
    },
    emailRules() {
      return [
        v => !v || /.+@.+\..+/.test(v) || this.$t('profile.invalidEmail')
      ]
    }
  },
  methods: {
    async handleRegister() {
      const { valid } = await this.$refs.form.validate()
      if (!valid) {
        this.showSnackbar(this.$t('profile.fixErrors'), 'warning')
        return
      }

      this.loading = true
      try {
        const response = await fetch(`${API_URL}/register`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            username: this.username,
            password: this.password,
            department: this.department,
            identity: this.identity,
            gender: this.gender,
            email: this.email
          })
        })
        const data = await response.json()

        if (data.success && data.accessToken && data.refreshToken) {
          auth.login(data.user, data.accessToken, data.refreshToken)
          this.showSnackbar(this.$t('auth.registerSuccess'), 'success')
          setTimeout(() => {
            this.$router.push({ name: 'Home' })
          }, 1000)
        } else {
          this.showSnackbar(data.message || 'Registration failed', 'error')
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
