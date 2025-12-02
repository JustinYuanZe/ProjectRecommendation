<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card class="pa-6" elevation="4">
          <v-card-title class="text-h4 text-center mb-4">
            <v-icon left color="primary">mdi-clipboard-list</v-icon>
            Career Assessment Test
          </v-card-title>

          <v-card-subtitle class="text-center mb-4">
            Question {{ currentQuestion + 1 }} / {{ questions.length }}
          </v-card-subtitle>

          <v-progress-linear :model-value="progress" color="primary" height="8" class="mb-6"></v-progress-linear>

          <div v-if="loading" class="text-center py-8">
            <v-progress-circular indeterminate color="primary"></v-progress-circular>
            <p class="mt-4">Loading questions...</p>
          </div>

          <div v-else-if="!showResults && questions.length > 0">
            <!-- Part Header -->
            <v-alert v-if="showPartHeader" type="info" variant="tonal" class="mb-4">
              <div class="font-weight-bold">Part {{ questions[currentQuestion].part }}: {{ questions[currentQuestion].partTitle }}</div>
              <div class="text-body-2 mt-1">{{ questions[currentQuestion].partObjective }}</div>
            </v-alert>

            <v-card class="pa-4 mb-6" elevation="2">
              <v-chip size="small" color="primary" class="mb-2">{{ questions[currentQuestion].id }}</v-chip>
              <v-card-text class="text-h6">
                {{ questions[currentQuestion].question }}
              </v-card-text>
            </v-card>

            <div class="rating-scale mb-6">
              <v-radio-group v-model="answers[questions[currentQuestion].id]" inline class="justify-center">
                <div class="scale-options">
                  <label v-for="option in ratingOptions" :key="option.value" class="scale-option" :class="{ 'selected': answers[questions[currentQuestion].id] === option.value }">
                    <v-radio :value="option.value" class="scale-radio"></v-radio>
                    <span class="scale-text">{{ option.text }}</span>
                  </label>
                </div>
              </v-radio-group>
            </div>

            <v-card-actions class="justify-space-between">
              <v-btn color="secondary" :disabled="currentQuestion === 0" @click="previousQuestion"
                prepend-icon="mdi-arrow-left">
                Previous
              </v-btn>

              <v-btn v-if="currentQuestion < questions.length - 1" color="primary" :disabled="answers[questions[currentQuestion].id] === undefined"
                @click="nextQuestion" append-icon="mdi-arrow-right">
                Next
              </v-btn>

              <v-btn v-else color="success" :disabled="answers[questions[currentQuestion].id] === undefined" @click="finishTest"
                prepend-icon="mdi-check">
                Complete
              </v-btn>
            </v-card-actions>
          </div>

          <div v-else-if="showResults" class="text-center">
            <v-icon color="success" size="64">mdi-check-circle</v-icon>
            <h3 class="text-h5 mt-4 mb-4">Assessment completed!</h3>
            <v-btn color="primary" size="large" :to="{ name: 'Results' }" prepend-icon="mdi-chart-line">
              View Results
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
  name: 'CareerTest',
  data() {
    return {
      currentQuestion: 0,
      answers: {},
      showResults: false,
      questions: [],
      loading: true,
      ratingOptions: [
        { value: -2, text: 'Strongly Disagree' },
        { value: -1, text: 'Disagree' },
        { value: 0, text: 'Neutral' },
        { value: 1, text: 'Agree' },
        { value: 2, text: 'Strongly Agree' }
      ]
    }
  },
  computed: {
    progress() {
      return ((this.currentQuestion + 1) / this.questions.length) * 100
    },
    showPartHeader() {
      if (this.questions.length === 0) return false
      if (this.currentQuestion === 0) return true
      const currentPart = this.questions[this.currentQuestion].part
      const prevPart = this.questions[this.currentQuestion - 1]?.part
      return currentPart !== prevPart
    }
  },
  async mounted() {
    await this.loadQuestions()
    const savedAnswers = localStorage.getItem('careerTestAnswers')
    if (savedAnswers) {
      this.answers = JSON.parse(savedAnswers)
    }
  },
  methods: {
    async loadQuestions() {
      try {
        const response = await fetch(`${API_URL}/questions`)
        const data = await response.json()
        if (data.success) {
          this.questions = data.questions
        }
      } catch (error) {
        console.error('Failed to load questions:', error)
        this.questions = []
      } finally {
        this.loading = false
      }
    },
    nextQuestion() {
      if (this.currentQuestion < this.questions.length - 1) {
        this.currentQuestion++
      }
      this.saveAnswers()
    },
    previousQuestion() {
      if (this.currentQuestion > 0) {
        this.currentQuestion--
      }
    },
    saveAnswers() {
      localStorage.setItem('careerTestAnswers', JSON.stringify(this.answers))
    },
    async finishTest() {
      this.saveAnswers()
      await this.calculateResults()
      this.showResults = true
    },
    async calculateResults() {
      // Calculate scores by category
      const categoryScores = {
        technical: 0,
        business: 0,
        creative: 0,
        interdisciplinary: 0
      }

      // Process each answer
      this.questions.forEach(question => {
        const answer = this.answers[question.id]
        if (answer !== undefined) {
          const category = question.category
          categoryScores[category] = (categoryScores[category] || 0) + answer
        }
      })

      const results = this.generateCareerRecommendations(categoryScores)
      localStorage.setItem('careerResults', JSON.stringify(results))

      if (auth.isLoggedIn && auth.user && auth.accessToken) {
        try {
          const response = await fetch(`${API_URL}/test-results`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': auth.getAuthHeader()
            },
            body: JSON.stringify({
              userId: auth.user.id,
              answers: this.answers,
              results
            })
          })
          const data = await response.json()
          if (data.success) {
            console.log('Test results saved to database')
          }
        } catch (error) {
          console.error('Failed to save test results:', error)
        }
      }

      return results
    },
    generateCareerRecommendations(categoryScores) {
      const careers = {
        technical: {
          title: "Software Engineering & Computer Science",
          careers: ["Software Developer", "Data Scientist", "Machine Learning Engineer", "Systems Architect", "Cybersecurity Specialist"],
          description: "Suitable for those who love technology, problem-solving, and building complex systems"
        },
        business: {
          title: "Business Information Systems & IT Management",
          careers: ["IT Project Manager", "Business Analyst", "IT Consultant", "Product Manager", "Data Analyst"],
          description: "Suitable for those with management skills and business understanding combined with technology"
        },
        creative: {
          title: "Digital Design & Media Technology",
          careers: ["UI/UX Designer", "Front-end Developer", "Digital Content Creator", "Interactive Media Designer", "Web Designer"],
          description: "Suitable for those with creativity and aesthetic sense in digital media"
        },
        interdisciplinary: {
          title: "Interdisciplinary IT & Emerging Technologies",
          careers: ["Tech Entrepreneur", "Innovation Consultant", "Digital Transformation Specialist", "EdTech Developer", "HealthTech Specialist"],
          description: "Suitable for those who thrive at the intersection of technology and other fields"
        }
      }

      // Calculate max possible scores per category
      const maxScorePerCategory = {}
      this.questions.forEach(q => {
        maxScorePerCategory[q.category] = (maxScorePerCategory[q.category] || 0) + 2
      })

      // Sort fields by score
      const sortedFields = Object.entries(categoryScores)
        .sort(([, a], [, b]) => b - a)
        .map(([field, score]) => ({
          field,
          score,
          maxScore: maxScorePerCategory[field] || 1,
          ...careers[field]
        }))

      return {
        topRecommendations: sortedFields,
        categoryScores
      }
    }
  }
}
</script>

<style scoped>
.rating-scale {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 32px 24px;
}

.scale-options {
  display: flex;
  justify-content: center;
  align-items: stretch;
  gap: 16px;
  width: 100%;
  flex-wrap: wrap;
}

.scale-option {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 20px 16px;
  min-width: 120px;
  border-radius: 12px;
  border: 2px solid #e0e0e0;
  background: white;
  cursor: pointer;
  transition: all 0.2s ease;
  flex: 1;
  max-width: 160px;
}

.scale-option:hover {
  border-color: #1976d2;
  background: #f5f5f5;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.scale-option.selected {
  border-color: #1976d2;
  background: #e3f2fd;
  box-shadow: 0 4px 12px rgba(25, 118, 210, 0.2);
}

.scale-radio {
  transform: scale(1.5);
}

.scale-radio :deep(.v-selection-control__input) {
  width: 24px;
  height: 24px;
}

.scale-text {
  font-size: 1rem;
  font-weight: 500;
  color: #424242;
  text-align: center;
  line-height: 1.3;
}

.scale-option.selected .scale-text {
  color: #1976d2;
  font-weight: 600;
}

@media (max-width: 960px) {
  .scale-options {
    gap: 12px;
  }
  
  .scale-option {
    min-width: 100px;
    padding: 16px 12px;
    max-width: 140px;
  }
  
  .scale-text {
    font-size: 0.9rem;
  }
}

@media (max-width: 600px) {
  .rating-scale {
    padding: 24px 16px;
  }
  
  .scale-options {
    gap: 8px;
  }
  
  .scale-option {
    min-width: 80px;
    padding: 14px 8px;
    max-width: 120px;
    gap: 8px;
  }
  
  .scale-text {
    font-size: 0.85rem;
  }
  
  .scale-radio {
    transform: scale(1.3);
  }
}
</style>
