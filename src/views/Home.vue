<template>
  <div class="home-page">
    <!-- Hero Section -->
    <section class="hero-section">
      <v-container fluid class="px-6">
        <v-row align="center" class="min-height-60vh">
          <v-col cols="12" md="6">
            <div class="hero-content">
              <h1 class="hero-title mb-4">
                University Career Advisory Platform
              </h1>
              <h2 class="hero-subtitle mb-6">
                Professional Career Guidance & Skills Assessment
              </h2>
              <p class="hero-description mb-8">
                Providing students with career diagnostics, career exploration, and learning recommendations<br>
                to help students understand themselves, explore careers, and enhance employment competitiveness.
              </p>
              <div class="hero-actions">
                <v-btn color="ucan-blue" size="x-large" class="mr-4 px-8" :to="{ name: 'Profile' }">
                  Start Exploring
                </v-btn>
                <v-btn color="ucan-orange" variant="outlined" size="x-large" class="px-8" :to="{ name: 'CareerTest' }">
                  Skills Assessment
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

    <!-- Exploration Section -->
    <section class="exploration-section py-16 bg-grey-lighten-5">
      <v-container>
        <div class="text-center mb-8">
          <h2 class="section-title mb-4">Start Your Career Journey</h2>
          <p class="section-subtitle">Discover the career path that matches your interests and strengths</p>
        </div>
        <v-row justify="center">
          <v-col cols="12" md="6" lg="5">
            <v-card class="pa-6 text-center" elevation="8" hover>
              <v-icon size="80" color="primary" class="mb-4">mdi-compass-outline</v-icon>
              <v-card-title class="text-h4 font-weight-bold mb-3">
                Career Interest Exploration
              </v-card-title>
              <v-card-subtitle class="text-h6 mb-6 text-wrap">
                Which career type suits my interests, traits, and preferences?
              </v-card-subtitle>
              <v-card-text class="text-body-1 mb-4">
                Take our comprehensive assessment to discover careers that align with your unique personality,
                skills, and aspirations. Get personalized recommendations based on your responses.
              </v-card-text>
              <v-card-actions class="justify-center">
                <v-btn color="primary" variant="elevated" size="x-large" @click="handleStartTest"
                  prepend-icon="mdi-play-circle" class="px-8">
                  Start Assessment
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Features Section -->
    <section class="features-section py-16">
      <v-container fluid class="px-6">
        <div class="text-center mb-12">
          <h2 class="section-title mb-4">Core Platform Features</h2>
          <p class="section-subtitle">Comprehensive Career Development Support System</p>
        </div>

        <v-row>
          <v-col cols="12" md="4" v-for="(feature, index) in features" :key="index">
            <v-card class="feature-card h-100" elevation="2" hover>
              <v-card-text class="text-center pa-8">
                <div class="feature-icon mb-4">
                  <v-icon :color="feature.color" size="64">{{ feature.icon }}</v-icon>
                </div>
                <h3 class="feature-title mb-3">{{ feature.title }}</h3>
                <p class="feature-description">{{ feature.description }}</p>
              </v-card-text>
              <v-card-actions class="justify-center pb-6">
                <v-btn :color="feature.color" variant="outlined" :to="feature.link">
                  Learn More
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </section>


    <!-- Login Required Modal -->
    <v-dialog v-model="loginDialog" max-width="500">
      <v-card>
        <v-card-title class="text-h5 bg-primary text-white d-flex align-center">
          <v-icon class="mr-2">mdi-lock-alert</v-icon>
          Authentication Required
        </v-card-title>
        <v-card-text class="pa-6">
          <v-alert type="info" variant="tonal" class="mb-4">
            You need to be logged in to take the career assessment test.
          </v-alert>
          <p class="text-body-1 mb-2">
            Please log in to save your test results and track your progress.
          </p>
          <p class="text-body-2 text-grey">
            Don't have an account? You can register for free!
          </p>
        </v-card-text>
        <v-card-actions class="pa-4 pt-0">
          <v-btn color="grey-darken-1" variant="text" @click="loginDialog = false">
            Cancel
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn color="secondary" variant="outlined" @click="$router.push({ name: 'Register' })">
            Register
          </v-btn>
          <v-btn color="primary" variant="elevated" @click="$router.push({ name: 'Login' })">
            Login
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
      // public assets are served at root path — use /p1.png
      heroImage: '/p1.png',
      features: [
        {
          icon: 'mdi-compass-outline',
          color: 'ucan-blue',
          title: 'Career Exploration',
          description: 'Through scientific assessment tools, help you understand personal interests, personality traits, and career directions to find the most suitable development path.',
          link: { name: 'Profile' }
        },
        {
          icon: 'mdi-brain',
          color: 'ucan-orange',
          title: 'Skills Assessment',
          description: 'Evaluate your professional skills, core competencies, and work potential, providing personalized ability analysis reports.',
          link: { name: 'CareerTest' }
        },
        {
          icon: 'mdi-school-outline',
          color: 'ucan-green',
          title: 'Learning Recommendations',
          description: 'Provide customized learning suggestions and competency enhancement plans based on assessment results to help you achieve career goals.',
          link: { name: 'Results' }
        }
      ],
      newsItems: [
        {
          image: '/vite.svg',
          date: '2025.01.15',
          title: 'Advisory System Platform Upgrade',
          excerpt: 'New AI-powered recommendation features provide more accurate career advice and learning path planning.'
        },
        {
          image: '/vite.svg',
          date: '2025.01.10',
          title: '2025 Employment Trend Report',
          excerpt: 'Analysis of popular careers and required skills for the next five years to help students prepare for their careers.'
        },
        {
          image: '/vite.svg',
          date: '2025.01.05',
          title: 'University-Industry Collaboration Results',
          excerpt: 'Showcasing the achievements of industry-academia cooperation in talent development, promoting practical education goals.'
        }
      ],
      loginDialog: false
    }
  },
  mounted() {
    // Check if we should show login dialog from router guard
    if (this.$route.query.showLogin === 'true') {
      this.loginDialog = true
      // Clean up the URL
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
    },
    handleLoginSuccess() {
      // Check if there's a redirect destination
      const redirectPath = sessionStorage.getItem('redirectAfterLogin')
      if (redirectPath) {
        sessionStorage.removeItem('redirectAfterLogin')
        this.$router.push(redirectPath)
      }
    }
  }
}
</script>

<style scoped>
/* Hero Section */
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
  font-size: 3rem;
  font-weight: 700;
  color: #1565C0;
  line-height: 1.2;
}

.hero-subtitle {
  font-size: 1.5rem;
  font-weight: 400;
  color: #37474F;
  line-height: 1.3;
}

.hero-description {
  font-size: 1.1rem;
  color: #757575;
  line-height: 1.6;
}

.hero-actions {
  margin-top: 2rem;
}

.hero-illustration {
  filter: drop-shadow(0 10px 30px rgba(21, 101, 192, 0.2));
}

/* Features Section */
.features-section {
  background: #ffffff;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #212121;
}

.section-subtitle {
  font-size: 1.2rem;
  color: #757575;
}

.feature-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border-radius: 12px;
  overflow: hidden;
}

.feature-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 40px rgba(21, 101, 192, 0.15) !important;
}

.feature-icon {
  background: rgba(21, 101, 192, 0.1);
  border-radius: 50%;
  width: 120px;
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
}

.feature-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #212121;
}

.feature-description {
  color: #757575;
  line-height: 1.6;
}

/* Statistics Section */
.stats-section {
  background: linear-gradient(135deg, #1565C0 0%, #0D47A1 100%);
  color: white;
}

.stat-item {
  padding: 2rem 1rem;
}

.stat-number {
  font-size: 3rem;
  font-weight: 700;
  color: white;
  margin-bottom: 0.5rem;
}

.stat-label {
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.9);
}

/* News Section */
.news-section {
  background: #f8f9fa;
}

.news-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border-radius: 12px;
  overflow: hidden;
}

.news-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1) !important;
}

.news-date {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: rgba(21, 101, 192, 0.9);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 500;
}

/* Responsive Design */
@media (max-width: 768px) {
  .hero-title {
    font-size: 2rem;
  }

  .hero-subtitle {
    font-size: 1.2rem;
  }

  .section-title {
    font-size: 2rem;
  }

  .stat-number {
    font-size: 2rem;
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

@media (max-width: 480px) {
  .hero-title {
    font-size: 1.75rem;
  }

  .feature-icon {
    width: 80px;
    height: 80px;
  }

  .feature-icon .v-icon {
    font-size: 2rem !important;
  }
}
</style>
