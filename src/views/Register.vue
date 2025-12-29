<template>
  <v-container class="register-container fill-height">
    <v-row justify="center" align="center" class="fill-height">
      <v-col cols="12" sm="10" md="6" lg="5" xl="4">
        <v-card elevation="8" class="register-card" rounded="lg">
          <!-- Header with gradient -->
          <div class="register-header">
            <v-icon size="48" color="white" class="mb-2">mdi-account-plus</v-icon>
            <h1 class="text-h5 font-weight-bold text-white mb-1">{{ $t('auth.registerTitle') }}</h1>
            <p class="text-body-2 text-white text-opacity-90">{{ $t('auth.registerSubtitle') }}</p>
          </div>

          <v-card-text class="pa-6">
            <v-form ref="form" @submit.prevent="handleRegister" v-model="valid">
              <!-- Account Information Section -->
              <div class="form-section mb-4">
                <h3 class="text-subtitle-1 font-weight-bold text-primary mb-3">
                  <v-icon size="20" color="primary" class="mr-1">mdi-account-circle</v-icon>
                  {{ $t('auth.accountInfo') || 'Account Information' }}
                </h3>

                <v-text-field v-model="username" :label="$t('auth.username')" prepend-inner-icon="mdi-account"
                  type="text" :rules="usernameRules" variant="outlined" color="primary" class="mb-2" required
                  hint="3-50 characters" persistent-hint></v-text-field>

                <v-text-field v-model="password" :label="$t('auth.password')" prepend-inner-icon="mdi-lock"
                  :type="showPassword ? 'text' : 'password'"
                  :append-inner-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                  @click:append-inner="showPassword = !showPassword" :rules="passwordRules" variant="outlined"
                  color="primary" class="mb-2" required hint="Minimum 6 characters" persistent-hint></v-text-field>

                <v-text-field v-model="confirmPassword" :label="$t('auth.confirmPassword')"
                  prepend-inner-icon="mdi-lock-check" :type="showConfirmPassword ? 'text' : 'password'"
                  :append-inner-icon="showConfirmPassword ? 'mdi-eye' : 'mdi-eye-off'"
                  @click:append-inner="showConfirmPassword = !showConfirmPassword" :rules="confirmPasswordRules"
                  variant="outlined" color="primary" required></v-text-field>
              </div>

              <!-- Personal Information Section -->
              <div class="form-section mb-4">
                <h3 class="text-subtitle-1 font-weight-bold text-primary mb-3">
                  <v-icon size="20" color="primary" class="mr-1">mdi-card-account-details</v-icon>
                  {{ $t('auth.personalInfo') || 'Personal Information' }}
                </h3>

                <v-select v-model="department" :items="departments" :label="$t('auth.department')"
                  prepend-inner-icon="mdi-school" :rules="requiredRules" variant="outlined" color="primary" class="mb-2"
                  required></v-select>

                <v-text-field v-model="email" :label="$t('profile.email')" prepend-inner-icon="mdi-email" type="email"
                  :rules="emailRules" variant="outlined" color="primary" class="mb-3" hint="Optional"
                  persistent-hint></v-text-field>

                <!-- Identity Selection with Cards -->
                <div class="mb-3">
                  <label class="text-caption text-grey-darken-2 font-weight-bold mb-2 d-block">
                    {{ $t('profile.identity') }}
                  </label>
                  <v-chip-group v-model="identity" mandatory color="primary" class="identity-chips">
                    <v-chip value="student" filter variant="outlined">
                      <v-icon start>mdi-school</v-icon>
                      {{ $t('profile.student') }}
                    </v-chip>
                    <v-chip value="Unemployed" filter variant="outlined">
                      <v-icon start>mdi-briefcase-search</v-icon>
                      {{ $t('profile.unemployed') }}
                    </v-chip>
                    <v-chip value="employed" filter variant="outlined">
                      <v-icon start>mdi-briefcase</v-icon>
                      {{ $t('profile.employed') }}
                    </v-chip>
                  </v-chip-group>
                </div>

                <!-- Gender Selection with Cards -->
                <div class="mb-2">
                  <label class="text-caption text-grey-darken-2 font-weight-bold mb-2 d-block">
                    {{ $t('profile.gender') }}
                  </label>
                  <v-chip-group v-model="gender" mandatory color="primary" class="gender-chips">
                    <v-chip value="female" filter variant="outlined">
                      <v-icon start>mdi-gender-female</v-icon>
                      {{ $t('profile.female') }}
                    </v-chip>
                    <v-chip value="male" filter variant="outlined">
                      <v-icon start>mdi-gender-male</v-icon>
                      {{ $t('profile.male') }}
                    </v-chip>
                  </v-chip-group>
                </div>
              </div>

              <!-- Submit Button -->
              <v-btn color="primary" type="submit" :loading="loading" block size="large"
                class="mb-3 text-none font-weight-bold" elevation="2">
                <v-icon start>mdi-account-plus</v-icon>
                {{ loading ? $t('auth.registering') : $t('auth.registerButton') }}
              </v-btn>

              <!-- Login Link -->
              <div class="text-center">
                <v-divider class="mb-3"></v-divider>
                <span class="text-body-2 text-grey-darken-1">{{ $t('auth.haveAccount') }}</span>
                <router-link to="/login" class="ml-1 text-body-2 text-primary text-decoration-none font-weight-bold">
                  {{ $t('auth.loginNow') }}
                </router-link>
              </div>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Snackbar for notifications -->
    <v-snackbar v-model="snackbar.show" :color="snackbar.color" location="top" :timeout="3000">
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
import { API_ENDPOINTS } from '../config/api'

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
        const response = await fetch(API_ENDPOINTS.REGISTER, {
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

<style scoped>
.register-container {
  min-height: calc(100vh - 64px);
  background-color: #f5f5f5;
}

.register-card {
  overflow: hidden;
}

.register-header {
  background: linear-gradient(135deg, #1976d2 0%, #1565c0 100%);
  padding: 32px 24px;
  text-align: center;
}

.form-section {
  border-left: 3px solid #1976d2;
  padding-left: 12px;
}

.identity-chips,
.gender-chips {
  gap: 8px;
}

.identity-chips .v-chip,
.gender-chips .v-chip {
  flex: 1;
  min-width: 100px;
  justify-content: center;
}

/* Smooth transitions */
.v-text-field,
.v-select {
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
  .register-header {
    padding: 24px 16px;
  }

  .identity-chips .v-chip,
  .gender-chips .v-chip {
    min-width: 80px;
    font-size: 0.813rem;
  }
}
</style>
