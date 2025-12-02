<template>
  <v-container class="fill-height">
    <v-row justify="center" align="center">
      <v-col cols="12" sm="8" md="6">
        <v-card class="elevation-12">
          <v-toolbar color="primary" dark flat>
            <v-toolbar-title>Register</v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-form ref="form" @submit.prevent="handleRegister" v-model="valid">
              <v-text-field 
                v-model="username" 
                label="Username" 
                prepend-icon="mdi-account" 
                type="text"
                :rules="usernameRules"
                :counter="50"
                required></v-text-field>
              <v-text-field 
                v-model="password" 
                label="Password" 
                prepend-icon="mdi-lock" 
                :type="showPassword ? 'text' : 'password'"
                :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                @click:append="showPassword = !showPassword"
                :rules="passwordRules"
                hint="Must be at least 6 characters with uppercase, lowercase, and number"
                persistent-hint
                required></v-text-field>
              <v-text-field 
                v-model="confirmPassword" 
                label="Confirm Password" 
                prepend-icon="mdi-lock-check" 
                :type="showConfirmPassword ? 'text' : 'password'"
                :append-icon="showConfirmPassword ? 'mdi-eye' : 'mdi-eye-off'"
                @click:append="showConfirmPassword = !showConfirmPassword"
                :rules="confirmPasswordRules"
                required></v-text-field>
              <v-select 
                v-model="department" 
                :items="departments" 
                label="Department/Major" 
                prepend-icon="mdi-school"
                :rules="requiredRules"
                required></v-select>
              <v-radio-group v-model="identity" row>
                <label class="d-block mb-2">Identity</label>
                <v-radio label="student" value="student"></v-radio>
                <v-radio label="Unemployed" value="Unemployed"></v-radio>
                <v-radio label="employed" value="employed"></v-radio>
              </v-radio-group>

              <v-radio-group v-model="gender" row>
                <label class="d-block mb-2">Gender</label>
                <v-radio label="female" value="female"></v-radio>
                <v-radio label="male" value="male"></v-radio>
              </v-radio-group>

              <v-text-field 
                v-model="accountNumber" 
                label="Account number" 
                prepend-icon="mdi-account-box"
                :rules="accountNumberRules"
                :counter="50"></v-text-field>
              <v-text-field 
                v-model="name" 
                label="Name" 
                prepend-icon="mdi-account"
                :rules="nameRules"
                :counter="100"></v-text-field>

              <div class="d-flex">
                <v-select v-model="dobYear" :items="years" label="Year" class="mr-2" dense></v-select>
                <v-select v-model="dobMonth" :items="months" label="Month" class="mr-2" dense></v-select>
                <v-select v-model="dobDay" :items="days" label="Day" dense></v-select>
              </div>

              <v-text-field 
                v-model="email" 
                label="Email address" 
                prepend-icon="mdi-email"
                type="email"
                :rules="emailRules"
                :counter="100"></v-text-field>
              <v-text-field 
                v-model="mobilePhone" 
                label="Mobile Phone" 
                prepend-icon="mdi-phone"
                :rules="phoneRules"
                :counter="15"
                placeholder="e.g., 0981772612"></v-text-field>

              <div class="d-flex">
                <v-select v-model="enrollmentYear" :items="enrollmentYears" label="Enrollment Year" class="mr-2" dense></v-select>
                <v-select v-model="enrollmentLevel" :items="enrollmentLevels" label="Year/Level" dense></v-select>
              </div>

              <v-text-field 
                v-model="schoolCity" 
                label="School City"
                :rules="schoolCityRules"
                :counter="50"></v-text-field>
              <v-text-field 
                v-model="schoolName" 
                label="School Name"
                :rules="schoolNameRules"
                :counter="100"></v-text-field>

              <v-select v-model="durationOfStudy" :items="durations" label="Duration of study"></v-select>
              <v-text-field 
                v-model="departmentInstitute" 
                label="Department/Institute"
                :rules="departmentInstituteRules"
                :counter="100"></v-text-field>

              <div class="d-flex">
                <v-select v-model="yearClass" :items="yearClasses" label="Year/Class" class="mr-2" dense></v-select>
                <v-text-field 
                  v-model="studentId" 
                  label="Student ID"
                  :rules="studentIdRules"
                  :counter="20"></v-text-field>
              </div>

              <v-checkbox 
                v-model="agreedToTerms" 
                label="I agree to the Terms of Use"
                :rules="termsRules"></v-checkbox>
              <div class="text-center mt-3">
                <v-btn color="primary" type="submit" :loading="loading">Register</v-btn>
              </div>
            </v-form>
            <div class="text-center mt-4">
              <router-link to="/login">Already have an account? Login</router-link>
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
      accountNumber: '',
      name: '',
      dobYear: null,
      dobMonth: null,
      dobDay: null,
      email: '',
      mobilePhone: '',
      enrollmentYear: null,
      enrollmentLevel: null,
      schoolCity: '',
      schoolName: '',
      durationOfStudy: null,
      departmentInstitute: '',
      yearClass: null,
      studentId: '',
      agreedToTerms: false,
      // Validation rules
      usernameRules: [
        v => !!v || 'Username is required',
        v => (v && v.length >= 3) || 'Username must be at least 3 characters',
        v => (v && v.length <= 50) || 'Username must be less than 50 characters'
      ],
      passwordRules: [
        v => !!v || 'Password is required',
        v => (v && v.length >= 6) || 'Password must be at least 6 characters',
        v => (v && v.length <= 100) || 'Password must be less than 100 characters',
        v => (v && /[A-Z]/.test(v)) || 'Password must contain at least one uppercase letter',
        v => (v && /[a-z]/.test(v)) || 'Password must contain at least one lowercase letter',
        v => (v && /[0-9]/.test(v)) || 'Password must contain at least one number'
      ],
      confirmPasswordRules: [
        v => !!v || 'Please confirm your password',
        v => v === this.password || 'Passwords do not match'
      ],
      requiredRules: [
        v => !!v || 'This field is required'
      ],
      emailRules: [
        v => !v || /.+@.+\..+/.test(v) || 'Email must be valid',
        v => !v || v.length <= 100 || 'Email must be less than 100 characters'
      ],
      nameRules: [
        v => !v || v.length <= 100 || 'Name must be less than 100 characters',
        v => !v || /^[a-zA-Z\s'-]+$/.test(v) || 'Name can only contain letters, spaces, hyphens, and apostrophes'
      ],
      accountNumberRules: [
        v => !v || v.length <= 50 || 'Account number must be less than 50 characters',
        v => !v || /^[a-zA-Z0-9-_]+$/.test(v) || 'Account number can only contain letters, numbers, hyphens, and underscores'
      ],
      phoneRules: [
        v => !v || /^[0-9+\s()-]+$/.test(v) || 'Invalid phone number format',
        v => !v || v.length <= 15 || 'Phone number must be less than 15 characters',
        v => !v || v.replace(/\D/g, '').length >= 8 || 'Phone number must have at least 8 digits'
      ],
      schoolCityRules: [
        v => !v || v.length <= 50 || 'City name must be less than 50 characters',
        v => !v || /^[a-zA-Z\s'-]+$/.test(v) || 'City name can only contain letters, spaces, hyphens, and apostrophes'
      ],
      schoolNameRules: [
        v => !v || v.length <= 100 || 'School name must be less than 100 characters'
      ],
      departmentInstituteRules: [
        v => !v || v.length <= 100 || 'Department/Institute must be less than 100 characters'
      ],
      studentIdRules: [
        v => !v || v.length <= 20 || 'Student ID must be less than 20 characters',
        v => !v || /^[a-zA-Z0-9-]+$/.test(v) || 'Student ID can only contain letters, numbers, and hyphens'
      ],
      termsRules: [
        v => !!v || 'You must agree to the Terms of Use'
      ],
      years: [],
      months: [],
      days: [],
      enrollmentYears: [],
      enrollmentLevels: [1,2,3,4,5,6],
      durations: ['Bachelor','Master','Doctorate'],
      yearClasses: [1,2,3,4,5],
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
  created() {
    // populate date and enrollment lists
    const currentYear = new Date().getFullYear()
    for (let y = 1950; y <= currentYear; y++) this.years.push(y)
    for (let m = 1; m <= 12; m++) this.months.push(m)
    for (let d = 1; d <= 31; d++) this.days.push(d)
    for (let y = 2000; y <= currentYear; y++) this.enrollmentYears.push(y)
  },
  methods: {
    async handleRegister() {
      // Validate form first
      const { valid } = await this.$refs.form.validate()
      if (!valid) {
        this.showSnackbar('Please fix the form errors', 'warning')
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
            department: this.department
            ,
            // profile payload (match backend keys)
            identity: this.identity,
            gender: this.gender,
            accountNumber: this.accountNumber,
            name: this.name,
            dateOfBirth: this.dobYear && this.dobMonth && this.dobDay ? { year: this.dobYear, month: this.dobMonth, day: this.dobDay } : null,
            email: this.email,
            mobilePhone: this.mobilePhone,
            enrollmentYear: this.enrollmentYear,
            enrollmentLevel: this.enrollmentLevel,
            schoolCity: this.schoolCity,
            schoolName: this.schoolName,
            durationOfStudy: this.durationOfStudy,
            departmentInstitute: this.departmentInstitute,
            yearClass: this.yearClass,
            studentId: this.studentId,
            agreedToTerms: this.agreedToTerms
          })
        })
        const data = await response.json()

        if (data.success && data.accessToken && data.refreshToken) {
          auth.login(data.user, data.accessToken, data.refreshToken)
          this.showSnackbar('Registration successful', 'success')
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
