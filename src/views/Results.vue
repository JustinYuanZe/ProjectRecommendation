<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="10">
        <v-card class="pa-6" elevation="4">
          <v-card-title class="text-h4 text-center mb-6">
            <v-icon left color="success">mdi-chart-line</v-icon>
            Career Counseling Results
          </v-card-title>

          <div v-if="results">
            <!-- Career Recommendations -->
            <v-card class="mb-6" elevation="2">
              <v-card-title class="bg-success text-white">
                <v-icon left>mdi-star</v-icon>
                Suitable Career Recommendations
              </v-card-title>
              <v-card-text class="pa-0">
                <v-expansion-panels variant="accordion">
                  <v-expansion-panel v-for="(recommendation, index) in results.topRecommendations" :key="index">
                    <v-expansion-panel-title>
                      <div class="d-flex align-center">
                        <v-chip :color="getScoreColor(index)" class="mr-3" size="small">
                          #{{ index + 1 }}
                        </v-chip>
                        <div>
                          <div class="font-weight-bold">{{ recommendation.title }}</div>
                          <div class="text-caption text-grey">
                            Score: {{ recommendation.score }} / {{ recommendation.maxScore }}
                          </div>
                        </div>
                      </div>
                    </v-expansion-panel-title>
                    <v-expansion-panel-text>
                      <div class="pa-4">
                        <p class="mb-4">{{ recommendation.description }}</p>
                        <h4 class="mb-3">Specific Careers:</h4>
                        <v-row>
                          <v-col cols="12" md="6" v-for="career in recommendation.careers" :key="career">
                            <v-card class="pa-3" elevation="1" color="grey-lighten-5">
                              <div class="d-flex align-center">
                                <v-icon left color="primary">mdi-briefcase</v-icon>
                                <span class="font-weight-medium">{{ career }}</span>
                              </div>
                            </v-card>
                          </v-col>
                        </v-row>
                      </div>
                    </v-expansion-panel-text>
                  </v-expansion-panel>
                </v-expansion-panels>
              </v-card-text>
            </v-card>

            <!-- Skills Match Analysis -->
            <v-card class="mb-6" elevation="2">
              <v-card-title class="bg-info text-white">
                <v-icon left>mdi-target</v-icon>
                Category Score Analysis
              </v-card-title>
              <v-card-text class="pa-4">
                <div v-for="(recommendation, index) in results.topRecommendations" :key="index" class="mb-4">
                  <h4 class="mb-2">{{ recommendation.title }}</h4>
                  <div class="d-flex justify-space-between mb-1">
                    <span>Compatibility</span>
                    <span>{{ getPercentage(recommendation.score, recommendation.maxScore) }}%</span>
                  </div>
                  <v-progress-linear 
                    :model-value="getPercentage(recommendation.score, recommendation.maxScore)"
                    :color="getScoreColor(index)" 
                    height="8"
                  ></v-progress-linear>
                </div>
              </v-card-text>
            </v-card>

            <!-- Recommendations for Improvement -->
            <v-card class="mb-6" elevation="2">
              <v-card-title class="bg-orange text-white">
                <v-icon left>mdi-lightbulb</v-icon>
                Development Suggestions
              </v-card-title>
              <v-card-text class="pa-4">
                <v-alert type="info" variant="tonal" class="mb-4">
                  Based on your results, here are suggestions for career development:
                </v-alert>

                <v-list>
                  <v-list-item v-for="(tip, index) in developmentTips" :key="index" prepend-icon="mdi-check-circle">
                    <v-list-item-title>{{ tip }}</v-list-item-title>
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>

            <!-- Action Buttons -->
            <v-card-actions class="justify-center">
              <v-btn color="secondary" :to="{ name: 'CareerTest' }" prepend-icon="mdi-refresh">
                Retake Test
              </v-btn>

              <v-btn color="primary" @click="downloadResults" prepend-icon="mdi-download" class="ml-4">
                Download Results
              </v-btn>

              <v-btn color="success" :to="{ name: 'Home' }" prepend-icon="mdi-home" class="ml-4">
                Go Home
              </v-btn>
            </v-card-actions>
          </div>

          <div v-else class="text-center">
            <v-icon color="warning" size="64">mdi-alert</v-icon>
            <h3 class="text-h5 mt-4 mb-4">No results found</h3>
            <p class="mb-4">You need to complete the assessment test first.</p>
            <v-btn color="primary" :to="{ name: 'CareerTest' }" prepend-icon="mdi-clipboard-list">
              Take the Test
            </v-btn>
          </div>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { auth } from '../store/auth'
import { API_URL } from '../config/api'

export default {
  name: 'Results',
  data() {
    return {
      results: null
    }
  },
  computed: {
    developmentTips() {
      if (!this.results || !this.results.topRecommendations.length) return []

      const topField = this.results.topRecommendations[0]
      const tips = {
        technical: [
          "Learn new programming languages that fit current trends",
          "Participate in open source projects to gain experience",
          "Obtain reputable technology certifications",
          "Build an online portfolio showcasing your projects"
        ],
        business: [
          "Develop data analysis and reporting skills",
          "Take project management courses (PMP, Agile)",
          "Build professional networking relationships",
          "Join internship programs at companies"
        ],
        creative: [
          "Build a diverse creative portfolio",
          "Learn the latest professional design tools",
          "Join design communities for feedback",
          "Follow modern design and art trends"
        ],
        interdisciplinary: [
          "Explore emerging fields combining technology with other domains",
          "Develop strong communication skills for diverse audiences",
          "Stay informed about how technology impacts various industries",
          "Build a versatile skill set spanning technical and soft skills"
        ]
      }

      return tips[topField.field] || tips.technical
    }
  },
  mounted() {
    this.loadData()
  },
  methods: {
    async loadData() {
      if (auth.isLoggedIn && auth.user && auth.accessToken) {
        try {
          const response = await fetch(`${API_URL}/test-results/${auth.user.id}`, {
            headers: {
              'Authorization': auth.getAuthHeader()
            }
          })
          const data = await response.json()

          if (data.success && data.results.length > 0) {
            const latestResult = data.results[data.results.length - 1]
            this.results = latestResult.results
            localStorage.setItem('careerResults', JSON.stringify(latestResult.results))
            return
          }
        } catch (error) {
          console.error('Failed to load results from database:', error)
        }
      }

      const savedResults = localStorage.getItem('careerResults')
      if (savedResults) {
        this.results = JSON.parse(savedResults)
      }
    },
    getScoreColor(index) {
      const colors = ['success', 'info', 'warning', 'grey']
      return colors[index] || 'grey'
    },
    getPercentage(score, maxScore) {
      // Convert from -maxScore to +maxScore range to 0-100%
      const minScore = -maxScore
      const range = maxScore - minScore
      return Math.round(((score - minScore) / range) * 100)
    },
    downloadResults() {
      if (!this.results) return

      const content = this.generateResultsText()
      const blob = new Blob([content], { type: 'text/plain;charset=utf-8' })
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `career-assessment-results-${new Date().toISOString().split('T')[0]}.txt`
      link.click()
      window.URL.revokeObjectURL(url)
    },
    generateResultsText() {
      let content = "=== CAREER COUNSELING RESULTS ===\n\n"

      content += "CAREER RECOMMENDATIONS:\n"
      this.results.topRecommendations.forEach((rec, index) => {
        content += `\n${index + 1}. ${rec.title}\n`
        content += `   Description: ${rec.description}\n`
        content += `   Careers: ${rec.careers.join(', ')}\n`
        content += `   Score: ${rec.score}/${rec.maxScore}\n`
      })

      content += "\nDEVELOPMENT SUGGESTIONS:\n"
      this.developmentTips.forEach((tip, index) => {
        content += `${index + 1}. ${tip}\n`
      })

      content += `\nReport generated on: ${new Date().toLocaleString('en-US')}\n`

      return content
    }
  }
}
</script>
