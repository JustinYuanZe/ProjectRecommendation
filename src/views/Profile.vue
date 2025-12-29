<template>
  <v-container class="py-4">
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card class="pa-4" elevation="2">
          <v-card-title class="text-h6 text-center pb-2">
            <v-icon left color="primary" size="small">mdi-account-edit</v-icon>
            {{ $t('profile.title') }}
          </v-card-title>

          <v-card-subtitle class="text-center pb-3 text-caption">
            {{ $t('profile.subtitle', { username: user?.username, department: user?.department }) }}
          </v-card-subtitle>

          <v-form ref="form" @submit.prevent="saveProfile" v-model="valid">
            <v-row>
              <!-- Identity & Gender -->
              <v-col cols="12" md="6">
                <v-radio-group v-model="profile.identity" :label="$t('profile.identity')" row density="compact">
                  <v-radio :label="$t('profile.student')" value="student"></v-radio>
                  <v-radio :label="$t('profile.unemployed')" value="Unemployed"></v-radio>
                  <v-radio :label="$t('profile.employed')" value="employed"></v-radio>
                </v-radio-group>
              </v-col>

              <v-col cols="12" md="6">
                <v-radio-group v-model="profile.gender" :label="$t('profile.gender')" row density="compact">
                  <v-radio :label="$t('profile.female')" value="female"></v-radio>
                  <v-radio :label="$t('profile.male')" value="male"></v-radio>
                </v-radio-group>
              </v-col>

              <!-- Personal Information -->
              <v-col cols="12" md="6">
                <v-text-field v-model="profile.accountNumber" :label="$t('profile.accountNumber')"
                  prepend-icon="mdi-account-box" variant="outlined" density="compact"></v-text-field>
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field v-model="profile.name" :label="$t('profile.fullName')" prepend-icon="mdi-account"
                  variant="outlined" density="compact"></v-text-field>
              </v-col>

              <!-- Date of Birth -->
              <v-col cols="12">
                <label class="text-caption mb-1 d-block">{{ $t('profile.dateOfBirth') }}</label>
                <v-row dense>
                  <v-col cols="4">
                    <v-select v-model="dobYear" :items="years" :label="$t('profile.year')" variant="outlined"
                      density="compact"></v-select>
                  </v-col>
                  <v-col cols="4">
                    <v-select v-model="dobMonth" :items="months" :label="$t('profile.month')" variant="outlined"
                      density="compact"></v-select>
                  </v-col>
                  <v-col cols="4">
                    <v-select v-model="dobDay" :items="days" :label="$t('profile.day')" variant="outlined"
                      density="compact"></v-select>
                  </v-col>
                </v-row>
              </v-col>

              <!-- Contact Information -->
              <v-col cols="12" md="6">
                <v-text-field v-model="profile.email" :label="$t('profile.email')" prepend-icon="mdi-email" type="email"
                  :rules="emailRules" variant="outlined" density="compact"></v-text-field>
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field v-model="profile.mobilePhone" :label="$t('profile.mobilePhone')" prepend-icon="mdi-phone"
                  variant="outlined" density="compact"></v-text-field>
              </v-col>

              <!-- Enrollment Information -->
              <v-col cols="12">
                <v-divider class="my-3"></v-divider>
                <h3 class="text-body-1 font-weight-bold mb-2">{{ $t('profile.enrollmentInfo') }}</h3>
              </v-col>

              <v-col cols="12" md="6">
                <v-select v-model="profile.enrollmentYear" :items="enrollmentYears"
                  :label="$t('profile.enrollmentYear')" prepend-icon="mdi-calendar" variant="outlined"
                  density="compact"></v-select>
              </v-col>

              <v-col cols="12" md="6">
                <v-select v-model="profile.enrollmentLevel" :items="enrollmentLevels"
                  :label="$t('profile.enrollmentLevel')" prepend-icon="mdi-school" variant="outlined"
                  density="compact"></v-select>
              </v-col>

              <!-- School Information -->
              <v-col cols="12" md="6">
                <v-text-field v-model="profile.schoolCity" :label="$t('profile.schoolCity')" prepend-icon="mdi-city"
                  variant="outlined" density="compact"></v-text-field>
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field v-model="profile.schoolName" :label="$t('profile.schoolName')"
                  prepend-icon="mdi-school-outline" variant="outlined" density="compact"></v-text-field>
              </v-col>

              <!-- Academic Information -->
              <v-col cols="12" md="6">
                <v-select v-model="profile.durationOfStudy" :items="translatedDurations"
                  :label="$t('profile.durationOfStudy')" prepend-icon="mdi-book-open-page-variant" variant="outlined"
                  density="compact"></v-select>
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field v-model="profile.departmentInstitute" :label="$t('profile.departmentInstitute')"
                  prepend-icon="mdi-domain" variant="outlined" density="compact"></v-text-field>
              </v-col>

              <v-col cols="12" md="6">
                <v-select v-model="profile.yearClass" :items="yearClasses" :label="$t('profile.yearClass')"
                  prepend-icon="mdi-counter" variant="outlined" density="compact"></v-select>
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field v-model="profile.studentId" :label="$t('profile.studentId')"
                  prepend-icon="mdi-card-account-details" variant="outlined" density="compact"></v-text-field>
              </v-col>

              <!-- Career Path Section -->
              <v-col cols="12" v-if="profile.careerPath">
                <v-divider class="my-3"></v-divider>
                <h3 class="text-body-1 font-weight-bold mb-3">
                  <v-icon left color="primary" size="small" class="mr-1">mdi-compass-outline</v-icon>
                  Career Recommendations
                </h3>

                <v-alert v-if="profile.careerPath.aiSummary" color="deep-purple" variant="tonal" class="mb-4"
                  border="start" prominent>
                  <template v-slot:prepend>
                    <v-icon color="deep-purple">mdi-robot-excited</v-icon>
                  </template>
                  <div class="text-subtitle-2 font-weight-bold mb-1">AI Career Summary</div>
                  <div class="text-body-2">{{ profile.careerPath.aiSummary }}</div>
                </v-alert>

                <div v-if="profile.careerPath.recommendedCourses && profile.careerPath.recommendedCourses.length > 0">
                  <div class="text-subtitle-2 font-weight-bold mb-2 ml-1">
                    <v-icon size="small" color="indigo" class="mr-1">mdi-bookshelf</v-icon>
                    Recommended Courses ({{ profile.careerPath.recommendedCourses.length }})
                  </div>
                  <v-expansion-panels variant="accordion" class="mb-3">
                    <v-expansion-panel v-for="(course, idx) in profile.careerPath.recommendedCourses" :key="idx">
                      <v-expansion-panel-title class="py-2">
                        <div class="d-flex align-center w-100">
                          <v-chip size="x-small" color="primary" variant="flat" class="mr-2">{{ course.code }}</v-chip>
                          <span class="text-body-2 font-weight-bold flex-grow-1">{{ course.name }}</span>
                          <v-chip size="x-small" :color="course.match_score > 0.5 ? 'success' : 'info'" class="ml-2">
                            {{ Math.round((course.match_score || 0) * 100) }}% Match
                          </v-chip>
                        </div>
                      </v-expansion-panel-title>
                      <v-expansion-panel-text>
                        <div class="pa-2">
                          <div class="d-flex align-center mb-2 text-caption text-grey-darken-1">
                            <v-icon size="x-small" class="mr-1">mdi-domain</v-icon>
                            {{ course.department }}
                          </div>
                          <p class="text-body-2 mb-3" style="line-height: 1.6;">{{ course.description }}</p>
                          <v-divider class="mb-2"></v-divider>
                          <div class="d-flex flex-wrap align-center ga-2">
                            <v-chip size="x-small" variant="outlined" color="grey">
                              <v-icon start size="x-small">mdi-school</v-icon>
                              {{ course.credits }} Credits
                            </v-chip>
                            <v-chip size="x-small" variant="outlined" color="grey">
                              <v-icon start size="x-small">mdi-signal-cellular-3</v-icon>
                              Level {{ course.level }}
                            </v-chip>
                            <v-chip size="x-small" variant="outlined"
                              :color="course.taught_in_english ? 'success' : 'warning'">
                              <v-icon start size="x-small">mdi-translate</v-icon>
                              {{ course.taught_in_english ? 'English' : 'Local Language' }}
                            </v-chip>
                          </div>
                        </div>
                      </v-expansion-panel-text>
                    </v-expansion-panel>
                  </v-expansion-panels>
                </div>
              </v-col>

              <!-- Actions -->
              <v-col cols="12">
                <v-card-actions class="justify-center mt-3">
                  <v-btn color="secondary" :to="{ name: 'Home' }" prepend-icon="mdi-arrow-left" size="small">
                    {{ $t('common.back') }}
                  </v-btn>

                  <v-btn color="primary" type="submit" prepend-icon="mdi-content-save" class="ml-4" :loading="loading"
                    size="small">
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
import { API_ENDPOINTS } from '../config/api'

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
        studentId: '',
        careerPath: null
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
        studentId: p.studentId || '',
        careerPath: p.careerPath || null
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

        const response = await fetch(API_ENDPOINTS.USER_PROFILE(this.user.id), {
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
