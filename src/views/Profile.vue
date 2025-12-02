<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="10">
        <v-card class="pa-6" elevation="4">
          <v-card-title class="text-h4 text-center mb-4">
            <v-icon left color="primary">mdi-account-edit</v-icon>
            User Profile
          </v-card-title>

          <v-card-subtitle class="text-center mb-4">
            Username: {{ user?.username }} | Department: {{ user?.department }}
          </v-card-subtitle>

          <v-form ref="form" @submit.prevent="saveProfile" v-model="valid">
            <v-row>
              <!-- Identity & Gender -->
              <v-col cols="12" md="6">
                <v-radio-group v-model="profile.identity" label="Identity" row>
                  <v-radio label="Student" value="student"></v-radio>
                  <v-radio label="Unemployed" value="Unemployed"></v-radio>
                  <v-radio label="Employed" value="employed"></v-radio>
                </v-radio-group>
              </v-col>

              <v-col cols="12" md="6">
                <v-radio-group v-model="profile.gender" label="Gender" row>
                  <v-radio label="Female" value="female"></v-radio>
                  <v-radio label="Male" value="male"></v-radio>
                </v-radio-group>
              </v-col>

              <!-- Personal Information -->
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="profile.accountNumber"
                  label="Account Number"
                  prepend-icon="mdi-account-box"
                  variant="outlined"
                ></v-text-field>
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                  v-model="profile.name"
                  label="Full Name"
                  prepend-icon="mdi-account"
                  variant="outlined"
                ></v-text-field>
              </v-col>

              <!-- Date of Birth -->
              <v-col cols="12">
                <label class="text-subtitle-2 mb-2 d-block">Date of Birth</label>
                <v-row dense>
                  <v-col cols="4">
                    <v-select
                      v-model="dobYear"
                      :items="years"
                      label="Year"
                      variant="outlined"
                      density="compact"
                    ></v-select>
                  </v-col>
                  <v-col cols="4">
                    <v-select
                      v-model="dobMonth"
                      :items="months"
                      label="Month"
                      variant="outlined"
                      density="compact"
                    ></v-select>
                  </v-col>
                  <v-col cols="4">
                    <v-select
                      v-model="dobDay"
                      :items="days"
                      label="Day"
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
                  label="Email Address"
                  prepend-icon="mdi-email"
                  type="email"
                  :rules="emailRules"
                  variant="outlined"
                ></v-text-field>
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                  v-model="profile.mobilePhone"
                  label="Mobile Phone"
                  prepend-icon="mdi-phone"
                  variant="outlined"
                ></v-text-field>
              </v-col>

              <!-- Enrollment Information -->
              <v-col cols="12">
                <v-divider class="my-4"></v-divider>
                <h3 class="text-h6 mb-3">Enrollment Information</h3>
              </v-col>

              <v-col cols="12" md="6">
                <v-select
                  v-model="profile.enrollmentYear"
                  :items="enrollmentYears"
                  label="Enrollment Year"
                  prepend-icon="mdi-calendar"
                  variant="outlined"
                ></v-select>
              </v-col>

              <v-col cols="12" md="6">
                <v-select
                  v-model="profile.enrollmentLevel"
                  :items="enrollmentLevels"
                  label="Year/Level"
                  prepend-icon="mdi-school"
                  variant="outlined"
                ></v-select>
              </v-col>

              <!-- School Information -->
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="profile.schoolCity"
                  label="School City"
                  prepend-icon="mdi-city"
                  variant="outlined"
                ></v-text-field>
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                  v-model="profile.schoolName"
                  label="School Name"
                  prepend-icon="mdi-school-outline"
                  variant="outlined"
                ></v-text-field>
              </v-col>

              <!-- Academic Information -->
              <v-col cols="12" md="6">
                <v-select
                  v-model="profile.durationOfStudy"
                  :items="durations"
                  label="Duration of Study"
                  prepend-icon="mdi-book-open-page-variant"
                  variant="outlined"
                ></v-select>
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                  v-model="profile.departmentInstitute"
                  label="Department/Institute"
                  prepend-icon="mdi-domain"
                  variant="outlined"
                ></v-text-field>
              </v-col>

              <v-col cols="12" md="6">
                <v-select
                  v-model="profile.yearClass"
                  :items="yearClasses"
                  label="Year/Class"
                  prepend-icon="mdi-counter"
                  variant="outlined"
                ></v-select>
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                  v-model="profile.studentId"
                  label="Student ID"
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
                    Back
                  </v-btn>
                  
                  <v-btn
                    color="primary"
                    type="submit"
                    prepend-icon="mdi-content-save"
                    class="ml-4"
                    :loading="loading"
                  >
                    Save Changes
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
        <v-btn variant="text" @click="snackbar.show = false">Close</v-btn>
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
      durations: ['Bachelor', 'Master', 'Doctorate'],
      yearClasses: [1, 2, 3, 4, 5],
      emailRules: [
        v => !v || /.+@.+\..+/.test(v) || 'Email must be valid'
      ],
      snackbar: {
        show: false,
        text: '',
        color: 'success'
      }
    }
  },
  created() {
    // Populate date and enrollment lists
    const currentYear = new Date().getFullYear()
    for (let y = 1950; y <= currentYear; y++) this.years.push(y)
    for (let m = 1; m <= 12; m++) this.months.push(m)
    for (let d = 1; d <= 31; d++) this.days.push(d)
    for (let y = 2000; y <= currentYear; y++) this.enrollmentYears.push(y)

    // Load user data from auth store
    this.user = auth.user
    
    // Redirect to login if not authenticated
    if (!this.user || !auth.isLoggedIn) {
      this.$router.push({ name: 'Login' })
      return
    }

    if (this.user?.profile) {
      // Populate profile fields from user data
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

      // Parse dateOfBirth
      if (p.dateOfBirth && typeof p.dateOfBirth === 'object') {
        this.dobYear = p.dateOfBirth.year
        this.dobMonth = p.dateOfBirth.month
        this.dobDay = p.dateOfBirth.day
      }
    }
  },
  methods: {
    async saveProfile() {
      // Check if user is logged in
      if (!this.user || !this.user.id) {
        this.showSnackbar('You must be logged in to update your profile', 'error')
        this.$router.push({ name: 'Login' })
        return
      }

      // Validate form
      const { valid } = await this.$refs.form.validate()
      if (!valid) {
        this.showSnackbar('Please fix the form errors', 'warning')
        return
      }

      this.loading = true
      try {
        // Build dateOfBirth object
        const dateOfBirth = this.dobYear && this.dobMonth && this.dobDay
          ? { year: this.dobYear, month: this.dobMonth, day: this.dobDay }
          : null

        // Update user profile via API
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
          // Update local user object
          auth.user.profile = data.user.profile
          localStorage.setItem('user', JSON.stringify(auth.user))
          
          this.showSnackbar('Profile updated successfully', 'success')
        } else {
          this.showSnackbar(data.message || 'Failed to update profile', 'error')
        }
      } catch (error) {
        console.error('Profile update error:', error)
        this.showSnackbar('An error occurred while saving', 'error')
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
