<template>
  <v-container class="py-4">
    <v-row justify="center">
      <v-col cols="12" sm="10" md="8" lg="6">
        <v-card class="test-card" elevation="3">
          <div class="test-header pa-4 text-center">
            <v-icon color="white" size="28">mdi-clipboard-list</v-icon>
            <h1 class="text-h6 font-weight-bold text-white mt-2">Career Test</h1>
            <div class="text-body-2 text-white opacity-80 mt-1">
              Question {{ currentQuestion + 1 }} of {{ questions.length }}
            </div>
          </div>

          <v-progress-linear :model-value="progress" color="success" height="6"
            class="progress-bar"></v-progress-linear>

          <v-card-text class="pa-4">
            <div v-if="loading" class="text-center py-8">
              <v-progress-circular indeterminate color="primary" size="40"></v-progress-circular>
              <p class="mt-3 text-body-2 text-grey">Loading questions...</p>
            </div>

            <div v-else-if="!showResults && questions.length > 0">
              <v-alert v-if="showPartHeader" type="info" variant="tonal" density="compact" class="mb-4">
                <div class="text-body-2 font-weight-bold">
                  Part {{ questions[currentQuestion].part }}: {{ questions[currentQuestion].partTitle }}
                </div>
              </v-alert>

              <div class="question-box mb-5">
                <v-chip size="x-small" color="primary" variant="flat" class="mb-2">
                  {{ questions[currentQuestion].category ? questions[currentQuestion].category.toUpperCase() : 'GENERAL'
                  }}
                </v-chip>
                <p class="question-text">{{ questions[currentQuestion].question }}</p>
              </div>

              <div class="rating-scale">
                <v-radio-group v-model="answers[questions[currentQuestion].id]" class="ma-0">
                  <div class="scale-options">
                    <label v-for="option in ratingOptions" :key="option.value" class="scale-option"
                      :class="{ 'selected': answers[questions[currentQuestion].id] === option.value }"
                      @click="answers[questions[currentQuestion].id] = option.value">
                      <v-radio :value="option.value" class="scale-radio" hide-details></v-radio>
                      <span class="scale-text">{{ option.text }}</span>
                    </label>
                  </div>
                </v-radio-group>
              </div>

              <div class="d-flex justify-space-between mt-5">
                <v-btn variant="outlined" color="grey-darken-1" :disabled="currentQuestion === 0"
                  @click="previousQuestion" prepend-icon="mdi-arrow-left">
                  Previous
                </v-btn>

                <v-btn v-if="currentQuestion < questions.length - 1" color="primary"
                  :disabled="answers[questions[currentQuestion].id] === undefined" @click="nextQuestion"
                  append-icon="mdi-arrow-right">
                  Next
                </v-btn>

                <v-btn v-else color="success" :disabled="answers[questions[currentQuestion].id] === undefined"
                  :loading="isAnalyzing" @click="finishTest" prepend-icon="mdi-check">
                  {{ isAnalyzing ? 'Analyzing...' : 'Complete Test' }}
                </v-btn>
              </div>
            </div>

            <div v-else-if="showResults" class="text-center py-6">
              <v-icon color="success" size="56">mdi-check-circle</v-icon>
              <h2 class="text-h6 mt-4 mb-2">Test Completed</h2>
              <p class="text-body-2 text-grey mb-4">Your results are ready!</p>
              <v-btn color="primary" size="large" :to="{ name: 'Results' }" prepend-icon="mdi-chart-line">
                View Results
              </v-btn>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { auth } from '../store/auth'
import { API_ENDPOINTS } from '../config/api'



export default {
  name: 'CareerTest',
  data() {
    return {
      currentQuestion: 0,
      answers: {},
      showResults: false,
      questions: [],
      loading: true,
      isAnalyzing: false
    }
  },
  computed: {
    progress() {
      if (this.questions.length === 0) return 0;
      return ((this.currentQuestion + 1) / this.questions.length) * 100
    },
    showPartHeader() {
      if (this.questions.length === 0) return false
      if (this.currentQuestion === 0) return true
      const currentPart = this.questions[this.currentQuestion].part
      const prevPart = this.questions[this.currentQuestion - 1]?.part
      return currentPart !== prevPart
    },
    ratingOptions() {
      return [
        { value: -2, text: 'Strongly Disagree' },
        { value: -1, text: 'Disagree' },
        { value: 0, text: 'Neutral' },
        { value: 1, text: 'Agree' },
        { value: 2, text: 'Strongly Agree' }
      ]
    }
  },
  async mounted() {
    this.loadQuestions()
    const savedAnswers = localStorage.getItem('careerTestAnswers')
    if (savedAnswers) {
      this.answers = JSON.parse(savedAnswers)
    }
  },
  methods: {
    async loadQuestions() {
      this.loading = true
      try {
        const response = await fetch(API_ENDPOINTS.QUESTIONS)
        const data = await response.json()
        if (data.success) {
          this.questions = data.questions
        } else {
          console.error('Failed to load questions:', data.message)
          // Fallback if needed, but per user request we should use DB
        }
      } catch (error) {
        console.error('Error fetching questions:', error)
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
      this.isAnalyzing = true
      this.saveAnswers()
      await this.calculateResults()
      this.isAnalyzing = false
      this.showResults = true
    },
    async calculateResults() {
      const categoryScores = {
        technical: 0,
        business: 0,
        creative: 0,
        interdisciplinary: 0
      }

      const qaPayload = []
      const sanitizedAnswers = {}

      this.questions.forEach(question => {
        const answer = this.answers[question.id]
        if (answer !== undefined) {
          const category = question.category
          if (categoryScores[category] !== undefined) {
            categoryScores[category] += answer
          }

          qaPayload.push({
            question: question.question,
            score: answer
          })

          const safeId = question.id.replace(/\./g, '_')
          sanitizedAnswers[safeId] = answer
        }
      })

      let results = this.generateCareerRecommendations(categoryScores)

      try {
        const response = await fetch(API_ENDPOINTS.CAREER_ANALYSIS, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': auth.getAuthHeader()
          },
          body: JSON.stringify({ answers: qaPayload })
        })

        if (response.ok) {
          const aiData = await response.json()
          results.aiAnalysis = {
            summary: aiData.ai_summary,
            courses: aiData.courses
          }

          // Update local profile state if returned by backend
          if (aiData.profile && auth.user) {
            auth.user.profile = aiData.profile
            localStorage.setItem('user', JSON.stringify(auth.user))
          }
        }
      } catch (error) {
        console.warn('AI Analysis failed:', error)
      }

      localStorage.setItem('careerResults', JSON.stringify(results))

      if (auth.isLoggedIn && auth.user) {
        const userIdToSend = auth.user.id || auth.user._id || 'demo_user_id';
        const usernameToSend = auth.user.username || 'Demo User';

        fetch(API_ENDPOINTS.TEST_RESULTS, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': auth.getAuthHeader()
          },
          body: JSON.stringify({
            userId: userIdToSend,
            username: usernameToSend,
            answers: sanitizedAnswers,
            results: results
          })
        }).catch(err => console.log("Fail saving test history to database:", err));
      }

      return results
    },
    generateCareerRecommendations(categoryScores) {
      const careers = {
        technical: {
          title: "Software Engineering & Computer Science",
          careers: ["Software Developer", "Data Scientist", "Machine Learning Engineer", "Systems Architect", "Cybersecurity Specialist"],
          description: "Suitable for those who love technology and problem-solving"
        },
        business: {
          title: "Business Information Systems & IT Management",
          careers: ["IT Project Manager", "Business Analyst", "IT Consultant", "Product Manager", "Data Analyst"],
          description: "Suitable for those with management skills and business understanding"
        },
        creative: {
          title: "Digital Design & Media Technology",
          careers: ["UI/UX Designer", "Front-end Developer", "Digital Content Creator", "Interactive Media Designer", "Web Designer"],
          description: "Suitable for those with creativity in digital media"
        },
        interdisciplinary: {
          title: "Interdisciplinary IT & Emerging Technologies",
          careers: ["Tech Entrepreneur", "Innovation Consultant", "Digital Transformation Specialist", "EdTech Developer", "HealthTech Specialist"],
          description: "Suitable for those at the intersection of technology and other fields"
        }
      }

      const questionCountPerCategory = {}
      this.questions.forEach(q => {
        const cat = q.category || 'technical'
        questionCountPerCategory[cat] = (questionCountPerCategory[cat] || 0) + 1
      })

      const sortedFields = Object.entries(categoryScores)
        .map(([field, rawScore]) => {
          const count = questionCountPerCategory[field] || 1;
          const minPossible = count * -2;
          const maxPossible = count * 2;
          const range = maxPossible - minPossible;

          let percentage = 0;
          if (range > 0) {
            percentage = Math.round(((rawScore - minPossible) / range) * 100);
          }

          return {
            field,
            score: rawScore,
            maxScore: maxPossible,
            percentage: percentage,
            ...careers[field]
          }
        })
        .sort((a, b) => b.percentage - a.percentage)

      return {
        topRecommendations: sortedFields,
        categoryScores
      }
    }
  }
}
</script>

<style scoped>
.test-card {
  border-radius: 16px;
  overflow: hidden;
}

.test-header {
  background: linear-gradient(135deg, #1565C0 0%, #0D47A1 100%);
}

.progress-bar {
  border-radius: 0;
}

.question-box {
  background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf1 100%);
  border-radius: 12px;
  padding: 20px;
  border-left: 4px solid #1565C0;
}

.question-text {
  font-size: 1.05rem;
  line-height: 1.6;
  color: #333;
  margin: 0;
  font-weight: 500;
}

.rating-scale {
  background: #fafafa;
  border-radius: 12px;
  padding: 20px 16px;
}

.scale-options {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  width: 100%;
}

.scale-option {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 14px 8px;
  min-width: 0;
  flex: 1;
  border-radius: 10px;
  border: 2px solid #e0e0e0;
  background: white;
  cursor: pointer;
  transition: all 0.2s ease;
}

.scale-option:hover {
  border-color: #1976d2;
  background: #f0f7ff;
  transform: translateY(-2px);
}

.scale-option.selected {
  border-color: #1976d2;
  background: #e3f2fd;
  box-shadow: 0 4px 12px rgba(25, 118, 210, 0.25);
}

.scale-radio {
  margin: 0 !important;
  padding: 0 !important;
}

.scale-radio :deep(.v-selection-control__wrapper) {
  width: 22px;
  height: 22px;
}

.scale-text {
  font-size: 0.75rem;
  font-weight: 500;
  color: #555;
  text-align: center;
  line-height: 1.2;
}

.scale-option.selected .scale-text {
  color: #1565C0;
  font-weight: 600;
}

@media (max-width: 600px) {
  .scale-options {
    flex-wrap: wrap;
    gap: 8px;
  }

  .scale-option {
    flex: 0 0 calc(33.33% - 6px);
    padding: 12px 6px;
  }

  .scale-option:nth-child(4),
  .scale-option:nth-child(5) {
    flex: 0 0 calc(50% - 4px);
  }

  .scale-text {
    font-size: 0.7rem;
  }

  .question-text {
    font-size: 0.95rem;
  }
}

@media (min-width: 601px) and (max-width: 960px) {
  .scale-option {
    padding: 12px 6px;
  }

  .scale-text {
    font-size: 0.72rem;
  }
}
</style>