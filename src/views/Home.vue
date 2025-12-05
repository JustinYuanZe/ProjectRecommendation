<template>
  <div class="home-page">
    <!-- Hero Section -->
    <section class="hero-section">
      <v-container fluid class="px-6">
        <v-row align="center" class="min-height-60vh">
          <v-col cols="12" md="6">
            <div class="hero-content">
              <h1 class="hero-title mb-4">
                {{ $t('home.heroTitle') }}
              </h1>
              <p class="hero-description mb-8">
                {{ $t('home.heroSubtitle') }}
              </p>
              <div class="hero-actions">
                <v-btn color="ucan-blue" size="x-large" class="mr-4 px-8" :to="{ name: 'CareerTest' }">
                  {{ $t('home.startTest') }}
                </v-btn>
                <v-btn color="ucan-orange" variant="outlined" size="x-large" class="px-8" :to="{ name: 'Results' }">
                  {{ $t('home.viewResults') }}
                </v-btn>
              </div>
            </div>
          </v-col>
          <v-col cols="12" md="6">
            <div class="hero-image">
              <v-img :src="heroImage" height="400" contain class="hero-illustration"></v-img>
            </div>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Features Section -->
    <section class="features-section py-16">
      <v-container fluid class="px-6">
        <div class="text-center mb-12">
          <h2 class="section-title mb-4">{{ $t('home.featuresTitle') }}</h2>
        </div>

        <v-row>
          <v-col cols="12" md="6" lg="3" v-for="(feature, index) in features" :key="index">
            <v-card class="feature-card h-100" elevation="2" hover>
              <v-card-text class="text-center pa-6">
                <div class="feature-icon mb-4">
                  <v-icon :color="feature.color" size="48">{{ feature.icon }}</v-icon>
                </div>
                <h3 class="feature-title mb-3">{{ $t(feature.titleKey) }}</h3>
                <p class="feature-description">{{ $t(feature.descKey) }}</p>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Career Fields Section -->
    <section class="career-fields-section py-16 bg-grey-lighten-5">
      <v-container>
        <div class="text-center mb-8">
          <h2 class="section-title mb-4">{{ $t('home.careerFieldsTitle') }}</h2>
          <p class="section-subtitle">{{ $t('home.careerFieldsSubtitle') }}</p>
        </div>
        <v-row>
          <v-col cols="12" md="6" v-for="field in careerFields" :key="field.key">
            <v-card class="career-field-card h-100" elevation="3" hover>
              <v-card-text class="pa-6">
                <div class="d-flex align-center mb-4">
                  <v-avatar :color="field.color" size="56" class="mr-4">
                    <v-icon color="white" size="28">{{ field.icon }}</v-icon>
                  </v-avatar>
                  <div>
                    <v-chip :color="field.color" size="small" class="mb-1">{{ $t(field.labelKey) }}</v-chip>
                    <h3 class="text-h6 font-weight-bold">{{ $t(field.titleKey) }}</h3>
                  </div>
                </div>
                <p class="text-body-2 mb-3">{{ $t(field.descKey) }}</p>
                <p class="text-caption text-grey">{{ $t(field.careersKey) }}</p>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- CTA Section -->
    <section class="cta-section py-16">
      <v-container>
        <v-card class="cta-card pa-8 text-center" color="primary" dark>
          <h2 class="text-h4 font-weight-bold mb-4 text-white">{{ $t('home.ctaTitle') }}</h2>
          <p class="text-h6 mb-6 text-white opacity-90">{{ $t('home.ctaSubtitle') }}</p>
          <v-btn color="white" size="x-large" class="px-8" @click="handleStartTest">
            <span class="text-primary">{{ $t('home.ctaButton') }}</span>
          </v-btn>
        </v-card>
      </v-container>
    </section>

    <!-- Login Required Modal -->
    <v-dialog v-model="loginDialog" max-width="500">
      <v-card>
        <v-card-title class="text-h5 bg-primary text-white d-flex align-center">
          <v-icon class="mr-2">mdi-lock-alert</v-icon>
          {{ $t('auth.loginRequired') }}
        </v-card-title>
        <v-card-text class="pa-6">
          <v-alert type="info" variant="tonal" class="mb-4">
            {{ $t('auth.loginRequired') }}
          </v-alert>
          <p class="text-body-2 text-grey">
            {{ $t('auth.noAccount') }}
          </p>
        </v-card-text>
        <v-card-actions class="pa-4 pt-0">
          <v-btn color="grey-darken-1" variant="text" @click="loginDialog = false">
            {{ $t('common.cancel') }}
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn color="secondary" variant="outlined" @click="$router.push({ name: 'Register' })">
            {{ $t('nav.register') }}
          </v-btn>
          <v-btn color="primary" variant="elevated" @click="$router.push({ name: 'Login' })">
            {{ $t('nav.login') }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { auth } from '../store/auth'

export default {
  name: 'Home',
  data() {
    return {
      heroImage: '/p1.png',
      features: [
        {
          icon: 'mdi-clipboard-check-outline',
          color: 'primary',
          titleKey: 'home.feature1Title',
          descKey: 'home.feature1Desc'
        },
        {
          icon: 'mdi-account-star',
          color: 'success',
          titleKey: 'home.feature2Title',
          descKey: 'home.feature2Desc'
        },
        {
          icon: 'mdi-robot',
          color: 'info',
          titleKey: 'home.feature3Title',
          descKey: 'home.feature3Desc'
        },
        {
          icon: 'mdi-compass-outline',
          color: 'warning',
          titleKey: 'home.feature4Title',
          descKey: 'home.feature4Desc'
        }
      ],
      careerFields: [
        {
          key: 'technical',
          icon: 'mdi-code-braces',
          color: 'primary',
          labelKey: 'home.technical',
          titleKey: 'home.technicalTitle',
          descKey: 'home.technicalDesc',
          careersKey: 'home.technicalCareers'
        },
        {
          key: 'business',
          icon: 'mdi-briefcase',
          color: 'success',
          labelKey: 'home.business',
          titleKey: 'home.businessTitle',
          descKey: 'home.businessDesc',
          careersKey: 'home.businessCareers'
        },
        {
          key: 'creative',
          icon: 'mdi-palette',
          color: 'warning',
          labelKey: 'home.creative',
          titleKey: 'home.creativeTitle',
          descKey: 'home.creativeDesc',
          careersKey: 'home.creativeCareers'
        },
        {
          key: 'interdisciplinary',
          icon: 'mdi-lightbulb',
          color: 'info',
          labelKey: 'home.interdisciplinary',
          titleKey: 'home.interdisciplinaryTitle',
          descKey: 'home.interdisciplinaryDesc',
          careersKey: 'home.interdisciplinaryCareers'
        }
      ],
      loginDialog: false
    }
  },
  mounted() {
    if (this.$route.query.showLogin === 'true') {
      this.loginDialog = true
      this.$router.replace({ name: 'Home' })
    }
  },
  methods: {
    handleStartTest() {
      if (auth.isLoggedIn) {
        this.$router.push({ name: 'CareerTest' })
      } else {
        this.loginDialog = true
      }
    }
  }
}
</script>

<style scoped>
.hero-section {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  min-height: 70vh;
  display: flex;
  align-items: center;
}

.min-height-60vh {
  min-height: 60vh;
}

.hero-title {
  font-size: 2.75rem;
  font-weight: 700;
  color: #1565C0;
  line-height: 1.2;
}

.hero-description {
  font-size: 1.2rem;
  color: #757575;
  line-height: 1.6;
}

.hero-illustration {
  filter: drop-shadow(0 10px 30px rgba(21, 101, 192, 0.2));
}

.features-section {
  background: #ffffff;
}

.section-title {
  font-size: 2.25rem;
  font-weight: 700;
  color: #212121;
}

.section-subtitle {
  font-size: 1.1rem;
  color: #757575;
}

.feature-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border-radius: 12px;
}

.feature-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 40px rgba(21, 101, 192, 0.15) !important;
}

.feature-icon {
  background: rgba(21, 101, 192, 0.1);
  border-radius: 50%;
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
}

.feature-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #212121;
}

.feature-description {
  color: #757575;
  line-height: 1.6;
  font-size: 0.95rem;
}

.career-field-card {
  transition: transform 0.3s ease;
  border-radius: 12px;
}

.career-field-card:hover {
  transform: translateY(-4px);
}

.cta-card {
  border-radius: 16px;
  background: linear-gradient(135deg, #1565C0 0%, #0D47A1 100%) !important;
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2rem;
  }

  .section-title {
    font-size: 1.75rem;
  }

  .hero-actions {
    text-align: center;
  }

  .hero-actions .v-btn {
    margin: 0.5rem;
    width: 100%;
    max-width: 200px;
  }
}
</style>
