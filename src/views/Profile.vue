<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="10">
        <v-card class="pa-6" elevation="4">
          <v-card-title class="text-h4 text-center mb-4">
            <v-icon left color="primary">mdi-account-edit</v-icon>
            {{ $t('profile.title') }}
          </v-card-title>

          <v-card-subtitle class="text-center mb-4">
            {{ $t('profile.subtitle', { username: user?.username, department: user?.department }) }}
          </v-card-subtitle>

          <v-form ref="form" @submit.prevent="saveProfile" v-model="valid">
            <v-row>
              <!-- Identity & Gender -->
              <v-col cols="12" md="6">
                <v-radio-group v-model="profile.identity" :label="$t('profile.identity')" row>
                  <v-radio :label="$t('profile.student')" value="student"></v-radio>
                  <v-radio :label="$t('profile.unemployed')" value="Unemployed"></v-radio>
                  <v-radio :label="$t('profile.employed')" value="employed"></v-radio>
                </v-radio-group>
              </v-col>

              <v-col cols="12" md="6">
                <v-radio-group v-model="profile.gender" :label="$t('profile.gender')" row>
                  <v-radio :label="$t('profile.female')" value="female"></v-radio>
                  <v-radio :label="$t('profile.male')" value="male"></v-radio>
                </v-radio-group>
              </v-col>

              <!-- Personal Information -->
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="profile.accountNumber"
                  :label="$t('profile.accountNumber')"
                  prepend-icon="mdi-account-box"
                  variant="outlined"
                ></v-text-field>
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                  v-model="profile.name"
                  :label="$t('profile.fullName')"
                  prepend-icon="mdi-account"
                  variant="outlined"
                ></v-text-field>
              </v-col>

              <!-- Date of Birth -->
              <v-col cols="12">
                <label class="text-subtitle-2 mb-2 d-block">{{ $t('profile.dateOfBirth') }}</label>
                <v-row dense>
                  <v-col cols="4">
                    <v-select
                      v-model="dobYear"
                      :items="years"
                      :label="$t('profile.year')"
                      variant="outlined"
                      density="compact"
                    ></v-select>
                  </v-col>
                  <v-col cols="4">
                    <v-select
                      v-model="dobMonth"
                      :items="months"
                      :label="$t('profile.month')"
                      variant="outlined"
                      density="compact"
                    ></v-select>
                  </v-col>
                  <v-col cols="4">
                    <v-select
                      v-model="dobDay"
                      :items="days"
                      :label="$t('profile.day')"
                      variant="outlined"
                      density="compact"
                    ></v-select>
                  </v-col>
                </v-row>
              </v-col>

              <!-- Contact Information -->
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="profile.email"
                  :label="$t('profile.email')"
                  prepend-icon="mdi-email"
                  type="email"
                  :rules="emailRules"
                  variant="outlined"
                ></v-text-field>
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                  v-model="profile.mobilePhone"
                  :label="$t('profile.mobilePhone')"
                  prepend-icon="mdi-phone"
                  variant="outlined"
                ></v-text-field>
              </v-col>

              <!-- Enrollment Information -->
              <v-col cols="12">
                <v-divider class="my-4"></v-divider>
                <h3 class="text-h6 mb-3">{{ $t('profile.enrollmentInfo') }}</h3>
              </v-col>

              <v-col cols="12" md="6">
                <v-select
                  v-model="profile.enrollmentYear"
                  :items="enrollmentYears"
                  :label="$t('profile.enrollmentYear')"
                  prepend-icon="mdi-calendar"
                  variant="outlined"
                ></v-select>
              </v-col>

              <v-col cols="12" md="6">
                <v-select
                  v-model="profile.enrollmentLevel"
                  :items="enrollmentLevels"
                  :label="$t('profile.enrollmentLevel')"
                  prepend-icon="mdi-school"
                  variant="outlined"
                ></v-select>
              </v-col>

              <!-- School Information -->
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="profile.schoolCity"
                  :label="$t('profile.schoolCity')"
                  prepend-icon="mdi-city"
                  variant="outlined"
                ></v-text-field>
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                  v-model="profile.schoolName"
                  :label="$t('profile.schoolName')"
                  prepend-icon="mdi-school-outline"
                  variant="outlined"
                ></v-text-field>
              </v-col>

              <!-- Academic Information -->
              <v-col cols="12" md="6">
                <v-select
                  v-model="profile.durationOfStudy"
                  :items="translatedDurations"
                  :label="$t('profile.durationOfStudy')"
                  prepend-icon="mdi-book-open-page-variant"
                  variant="outlined"
                ></v-select>
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                  v-model="profile.departmentInstitute"
                  :label="$t('profile.departmentInstitute')"
                  prepend-icon="mdi-domain"
                  variant="outlined"
                ></v-text-field>
              </v-col>

              <v-col cols="12" md="6">
                <v-select
                  v-model="profile.yearClass"
                  :items="yearClasses"
                  :label="$t('profile.yearClass')"
                  prepend-icon="mdi-counter"
                  variant="outlined"
                ></v-select>
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                  v-model="profile.studentId"
                  :label="$t('profile.studentId')"
                  prepend-icon="mdi-card-account-details"
                  variant="outlined"
                ></v-text-field>
              </v-col>

              <!-- Actions -->
              <v-col cols="12">
                <v-card-actions class="justify-center mt-4">
                  <v-btn
                    color="secondary"
                    :to="{ name: 'Home' }"
                    prepend-icon="mdi-arrow-left"
                  >
                    {{ $t('common.back') }}
                  </v-btn>
                  
                  <v-btn
                    color="primary"
                    type="submit"
                    prepend-icon="mdi-content-save"
                    class="ml-4"
                    :loading="loading"
                  >
                    {{ loading ? $t('profile.saving') : $t('profile.saveChanges') }}
                  </v-btn>
                </v-card-actions>
              </v-col>
            </v-row>
          </v-form>
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
  name: 'Profile',
  data() {
    return {
      valid: false,
      loading: false,
      user: null,
      profile: {
        identity: 'student',
        gender: 'female',
        accountNumber: '',
        name: '',
        email: '',
        mobilePhone: '',
        enrollmentYear: null,
        enrollmentLevel: null,
        schoolCity: '',
        schoolName: '',
        durationOfStudy: null,
        departmentInstitute: '',
        yearClass: null,
        studentId: ''
      },
      dobYear: null,
      dobMonth: null,
      dobDay: null,
      years: [],
      months: [],
      days: [],
      enrollmentYears: [],
      enrollmentLevels: [1, 2, 3, 4, 5, 6],
      yearClasses: [1, 2, 3, 4, 5],
      snackbar: {
        show: false,
        text: '',
        color: 'success'
      }
    }
  },
  computed: {
    emailRules() {
      return [
        v => !v || /.+@.+\..+/.test(v) || this.$t('profile.invalidEmail')
      ]
    },
    translatedDurations() {
      return [
        { title: this.$t('profile.bachelor'), value: 'Bachelor' },
        { title: this.$t('profile.master'), value: 'Master' },
        { title: this.$t('profile.doctorate'), value: 'Doctorate' }
      ]
    }
  },
  created() {
    const currentYear = new Date().getFullYear()
    for (let y = 1950; y <= currentYear; y++) this.years.push(y)
    for (let m = 1; m <= 12; m++) this.months.push(m)
    for (let d = 1; d <= 31; d++) this.days.push(d)
    for (let y = 2000; y <= currentYear; y++) this.enrollmentYears.push(y)

    this.user = auth.user
    
    if (!this.user || !auth.isLoggedIn) {
      this.$router.push({ name: 'Login' })
      return
    }

    if (this.user?.profile) {
      const p = this.user.profile
      this.profile = {
        identity: p.identity || 'student',
        gender: p.gender || 'female',
        accountNumber: p.accountNumber || '',
        name: p.name || '',
        email: p.email || '',
        mobilePhone: p.mobilePhone || '',
        enrollmentYear: p.enrollment?.year || null,
        enrollmentLevel: p.enrollment?.level || null,
        schoolCity: p.school?.city || '',
        schoolName: p.school?.name || '',
        durationOfStudy: p.durationOfStudy || null,
        departmentInstitute: p.departmentInstitute || '',
        yearClass: p.yearClass || null,
        studentId: p.studentId || ''
      }

      if (p.dateOfBirth && typeof p.dateOfBirth === 'object') {
        this.dobYear = p.dateOfBirth.year
        this.dobMonth = p.dateOfBirth.month
        this.dobDay = p.dateOfBirth.day
      }
    }
  },
  methods: {
    async saveProfile() {
      if (!this.user || !this.user.id) {
        this.showSnackbar(this.$t('profile.loginRequired'), 'error')
        this.$router.push({ name: 'Login' })
        return
      }

      const { valid } = await this.$refs.form.validate()
      if (!valid) {
        this.showSnackbar(this.$t('profile.fixErrors'), 'warning')
        return
      }

      this.loading = true
      try {
        const dateOfBirth = this.dobYear && this.dobMonth && this.dobDay
          ? { year: this.dobYear, month: this.dobMonth, day: this.dobDay }
          : null

        const response = await fetch(`${API_URL}/users/${this.user.id}/profile`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': auth.getAuthHeader()
          },
          body: JSON.stringify({
            identity: this.profile.identity,
            gender: this.profile.gender,
            accountNumber: this.profile.accountNumber,
            name: this.profile.name,
            dateOfBirth,
            email: this.profile.email,
            mobilePhone: this.profile.mobilePhone,
            enrollmentYear: this.profile.enrollmentYear,
            enrollmentLevel: this.profile.enrollmentLevel,
            schoolCity: this.profile.schoolCity,
            schoolName: this.profile.schoolName,
            durationOfStudy: this.profile.durationOfStudy,
            departmentInstitute: this.profile.departmentInstitute,
            yearClass: this.profile.yearClass,
            studentId: this.profile.studentId
          })
        })

        const data = await response.json()

        if (data.success) {
          auth.user.profile = data.user.profile
          localStorage.setItem('user', JSON.stringify(auth.user))
          this.showSnackbar(this.$t('profile.updateSuccess'), 'success')
        } else {
          this.showSnackbar(data.message || this.$t('profile.updateError'), 'error')
        }
      } catch (error) {
        console.error('Profile update error:', error)
        this.showSnackbar(this.$t('profile.updateError'), 'error')
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
