<template>
  <div class="chatbot-container">
    <!-- Floating Button -->
    <v-btn
      v-if="!isOpen"
      class="chatbot-toggle-btn"
      color="primary"
      size="large"
      icon
      elevation="6"
      @click="toggleChat"
    >
      <v-icon size="28">mdi-chat</v-icon>
    </v-btn>

    <!-- Chat Window -->
    <v-card
      v-if="isOpen"
      class="chatbot-window"
      elevation="12"
      width="400"
      height="600"
    >
      <!-- Header -->
      <v-card-title class="chatbot-header d-flex align-center justify-space-between">
        <div class="d-flex align-center">
          <v-icon color="white" class="mr-2">mdi-robot-happy</v-icon>
          <span class="text-white font-weight-bold">Career Assistant</span>
        </div>
        <div>
          <v-btn
            icon
            variant="text"
            size="small"
            @click="clearChat"
            title="Clear chat"
          >
            <v-icon color="white" size="small">mdi-delete-outline</v-icon>
          </v-btn>
          <v-btn
            icon
            variant="text"
            size="small"
            @click="toggleChat"
            title="Close"
          >
            <v-icon color="white">mdi-close</v-icon>
          </v-btn>
        </div>
      </v-card-title>

      <!-- Messages Area -->
      <v-card-text class="chatbot-messages pa-0" ref="messagesContainer">
        <div v-if="messages.length === 0" class="welcome-section pa-4">
          <div class="text-center mb-4">
            <v-icon size="48" color="primary" class="mb-2">mdi-robot-happy</v-icon>
            <h3 class="text-h6 mb-1">Hi! I'm your Career Assistant</h3>
            <p class="text-body-2 text-grey">I can help you explore careers, prepare for interviews, and plan your professional journey.</p>
          </div>
          <div class="starter-questions">
            <p class="text-caption text-grey-darken-1 mb-2">Try asking:</p>
            <v-chip
              v-for="question in starterQuestions"
              :key="question"
              size="small"
              class="mr-1 mb-1"
              @click="handleQuickReply(question)"
              style="cursor: pointer;"
              variant="outlined"
              color="primary"
            >
              {{ question }}
            </v-chip>
          </div>
        </div>
        
        <div
          v-for="(message, index) in messages"
          :key="index"
          :class="['message', message.type]"
        >
          <div class="message-content">
            <div v-if="message.type === 'user'" class="message-bubble user-bubble">
              {{ message.text }}
            </div>
            <div v-else class="message-bubble bot-bubble">
              <div v-html="formatMessage(message.text)"></div>
              <div v-if="message.quickReplies && message.quickReplies.length > 0" class="quick-replies mt-2">
                <v-chip
                  v-for="(reply, idx) in message.quickReplies"
                  :key="idx"
                  size="small"
                  class="mr-1 mb-1"
                  @click="handleQuickReply(reply)"
                  style="cursor: pointer;"
                >
                  {{ reply }}
                </v-chip>
              </div>
            </div>
            <div class="message-time">{{ formatTime(message.timestamp) }}</div>
          </div>
        </div>

        <div v-if="loading" class="message bot">
          <div class="message-content">
            <div class="message-bubble bot-bubble">
              <v-progress-circular indeterminate size="20" color="primary"></v-progress-circular>
              <span class="ml-2">Thinking...</span>
            </div>
          </div>
        </div>
      </v-card-text>

      <!-- Input Area -->
      <v-card-actions class="chatbot-input pa-2">
        <v-text-field
          v-model="inputMessage"
          placeholder="Type your message..."
          variant="outlined"
          density="compact"
          hide-details
          @keyup.enter="sendMessage"
          :disabled="loading"
          class="flex-grow-1"
        ></v-text-field>
        <v-btn
          color="primary"
          icon
          @click="sendMessage"
          :disabled="!inputMessage.trim() || loading"
          class="ml-2"
        >
          <v-icon>mdi-send</v-icon>
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script>
import { sendMessage, buildContext } from '../services/chatbot'
import { auth } from '../store/auth'

export default {
  name: 'Chatbot',
  data() {
    return {
      isOpen: false,
      messages: [],
      inputMessage: '',
      loading: false,
      starterQuestions: [
        "What careers match my results?",
        "How do I prepare for tech interviews?",
        "What skills should I learn?",
        "Help me write a resume",
        "Best job search websites?"
      ]
    }
  },
  computed: {
    dynamicQuickReplies() {
      const results = this.getLatestResultSummary()
      if (results.hasCompletedQuiz) {
        return [
          `Tell me about ${results.topCareerField}`,
          "Skills I should learn",
          "Interview tips for my field",
          "View my full results"
        ]
      }
      return [
        "Take the career quiz",
        "What careers are in demand?",
        "How does the quiz work?"
      ]
    }
  },
  mounted() {
    // Load chat history from localStorage
    const savedMessages = localStorage.getItem('chatbotMessages')
    if (savedMessages) {
      try {
        this.messages = JSON.parse(savedMessages)
      } catch (e) {
        console.error('Failed to load chat history:', e)
      }
    }
  },
  watch: {
    isOpen(newVal) {
      if (newVal) {
        // Scroll to bottom when opening
        this.$nextTick(() => {
          this.scrollToBottom()
        })
      }
    },
    messages: {
      handler() {
        // Save messages to localStorage
        localStorage.setItem('chatbotMessages', JSON.stringify(this.messages))
        // Scroll to bottom when new message arrives
        this.$nextTick(() => {
          this.scrollToBottom()
        })
      },
      deep: true
    }
  },
  methods: {
    toggleChat() {
      this.isOpen = !this.isOpen
    },
    
    clearChat() {
      this.messages = []
      localStorage.removeItem('chatbotMessages')
    },
    
    async sendMessage() {
      if (!this.inputMessage.trim() || this.loading) return
      
      const userMessage = this.inputMessage.trim()
      this.inputMessage = ''
      
      // Add user message
      this.messages.push({
        type: 'user',
        text: userMessage,
        timestamp: new Date()
      })
      
      this.loading = true
      
      try {
        // Build context from current app state
        const currentPage = this.getCurrentPage()
        const testState = this.getTestState()
        const latestResultSummary = this.getLatestResultSummary()
        
        const context = buildContext(
          auth.user,
          currentPage,
          testState,
          latestResultSummary
        )
        
        // Send to chatbot service
        const response = await sendMessage(userMessage, context)
        
        // Use AI quick replies or fallback to context-aware defaults
        let quickReplies = response.quickReplies || []
        if (quickReplies.length === 0) {
          quickReplies = this.getContextAwareQuickReplies(userMessage)
        }
        
        // Add bot response
        this.messages.push({
          type: 'bot',
          text: response.reply,
          quickReplies: quickReplies,
          action: response.action,
          timestamp: new Date()
        })
        
        // Handle navigation action if present
        if (response.action && response.action.type === 'navigate') {
          setTimeout(() => {
            this.$router.push(response.action.target)
          }, 1000)
        }
      } catch (error) {
        console.error('Error sending message:', error)
        this.messages.push({
          type: 'bot',
          text: 'Sorry, I encountered an error. Please try again.',
          timestamp: new Date()
        })
      } finally {
        this.loading = false
      }
    },
    
    handleQuickReply(reply) {
      this.inputMessage = reply
      this.sendMessage()
    },
    
    formatMessage(text) {
      if (!text) return ''
      
      let formatted = text
      
      // Escape HTML first to prevent XSS
      formatted = formatted
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
      
      // Code blocks (```)
      formatted = formatted.replace(/```([\s\S]*?)```/g, '<pre class="code-block">$1</pre>')
      
      // Inline code (`)
      formatted = formatted.replace(/`([^`]+)`/g, '<code class="inline-code">$1</code>')
      
      // Bold (**text** or __text__)
      formatted = formatted.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
      formatted = formatted.replace(/__([^_]+)__/g, '<strong>$1</strong>')
      
      // Italic (*text* or _text_)
      formatted = formatted.replace(/\*([^*]+)\*/g, '<em>$1</em>')
      formatted = formatted.replace(/_([^_]+)_/g, '<em>$1</em>')
      
      // Process lines for lists
      const lines = formatted.split('\n')
      let inList = false
      let listType = null
      const processedLines = []
      
      for (let i = 0; i < lines.length; i++) {
        let line = lines[i]
        
        // Numbered list (1. item)
        const numberedMatch = line.match(/^(\d+)\.\s+(.+)$/)
        // Bullet list (* item or - item)
        const bulletMatch = line.match(/^\s*[\*\-]\s+(.+)$/)
        
        if (numberedMatch) {
          if (!inList || listType !== 'ol') {
            if (inList) processedLines.push(listType === 'ol' ? '</ol>' : '</ul>')
            processedLines.push('<ol class="chat-list">')
            inList = true
            listType = 'ol'
          }
          processedLines.push(`<li>${numberedMatch[2]}</li>`)
        } else if (bulletMatch) {
          if (!inList || listType !== 'ul') {
            if (inList) processedLines.push(listType === 'ol' ? '</ol>' : '</ul>')
            processedLines.push('<ul class="chat-list">')
            inList = true
            listType = 'ul'
          }
          processedLines.push(`<li>${bulletMatch[1]}</li>`)
        } else {
          if (inList) {
            processedLines.push(listType === 'ol' ? '</ol>' : '</ul>')
            inList = false
            listType = null
          }
          // Convert line breaks for non-list items
          if (line.trim()) {
            processedLines.push(line)
          } else {
            processedLines.push('<br>')
          }
        }
      }
      
      // Close any open list
      if (inList) {
        processedLines.push(listType === 'ol' ? '</ol>' : '</ul>')
      }
      
      // Join and handle remaining line breaks
      formatted = processedLines.join('\n')
      
      // Replace remaining newlines with <br> (but not inside lists)
      formatted = formatted.replace(/\n(?!<)/g, '<br>')
      formatted = formatted.replace(/\n</g, '<')
      
      return formatted
    },
    
    formatTime(timestamp) {
      const date = new Date(timestamp)
      return date.toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit' 
      })
    },
    
    scrollToBottom() {
      const container = this.$refs.messagesContainer
      if (container) {
        container.scrollTop = container.scrollHeight
      }
    },
    
    getCurrentPage() {
      const routeName = this.$route.name
      const pageMap = {
        'Home': 'Home',
        'CareerTest': 'CareerTest',
        'Results': 'Results',
        'Profile': 'Profile',
        'Login': 'Login',
        'Register': 'Register',
        'FAQ': 'FAQ',
        'About': 'About'
      }
      return pageMap[routeName] || 'Home'
    },
    
    getTestState() {
      // Try to get test state from CareerTest component or localStorage
      const savedAnswers = localStorage.getItem('careerTestAnswers')
      if (savedAnswers && this.$route.name === 'CareerTest') {
        try {
          const answers = JSON.parse(savedAnswers)
          const questionCount = Object.keys(answers).length
          // Estimate progress (this is approximate)
          return {
            testId: `test-${Date.now()}`,
            questionIndex: questionCount - 1,
            progress: questionCount / 50 // Assuming ~50 questions
          }
        } catch (e) {
          return null
        }
      }
      return null
    },
    
    getContextAwareQuickReplies(userMessage) {
      const lowerMsg = userMessage.toLowerCase()
      const results = this.getLatestResultSummary()
      
      // Career/job related queries
      if (lowerMsg.includes('career') || lowerMsg.includes('job') || lowerMsg.includes('result')) {
        if (results.hasCompletedQuiz) {
          return ['Skills to develop', 'Interview preparation', 'Job search tips']
        }
        return ['Take the career quiz', 'What careers are trending?']
      }
      
      // Interview related
      if (lowerMsg.includes('interview')) {
        return ['Common interview questions', 'Technical interview tips', 'Salary negotiation']
      }
      
      // Resume/CV related
      if (lowerMsg.includes('resume') || lowerMsg.includes('cv')) {
        return ['Resume format tips', 'What to include', 'LinkedIn optimization']
      }
      
      // Skills related
      if (lowerMsg.includes('skill') || lowerMsg.includes('learn')) {
        return ['Free learning resources', 'Recommended certifications', 'Project ideas']
      }
      
      // Default suggestions based on quiz status
      if (results.hasCompletedQuiz) {
        return ['Explain my results', 'Career advice', 'Next steps']
      }
      return ['Take career quiz', 'How does the quiz work?', 'Career options']
    },
    
    getLatestResultSummary() {
      // Try to get latest result from localStorage or API
      const savedResults = localStorage.getItem('careerResults')
      if (savedResults) {
        try {
          const results = JSON.parse(savedResults)
          if (results.topRecommendations && results.topRecommendations.length > 0) {
            const topRec = results.topRecommendations[0]
            const maxScore = topRec.maxScore || 10
            const score = topRec.score || 0
            // Calculate percentage (scores range from -maxScore to +maxScore)
            const percentage = Math.round(((score + maxScore) / (2 * maxScore)) * 100)
            
            // Build detailed scores string
            const detailedScores = results.topRecommendations
              .map(r => `${r.title || r.field}: ${r.score}/${r.maxScore}`)
              .join(', ')
            
            return {
              hasCompletedQuiz: true,
              resultId: `result-${Date.now()}`,
              topCareerField: topRec.title || topRec.field || 'Unknown',
              topCareers: topRec.careers || [],
              score: score,
              maxScore: maxScore,
              percentage: percentage,
              allRecommendations: results.topRecommendations.map(r => r.title || r.field).filter(Boolean),
              detailedScores: detailedScores,
              profileTags: results.topRecommendations.map(r => r.field).filter(Boolean),
              description: topRec.description || ''
            }
          }
        } catch (e) {
          return { hasCompletedQuiz: false }
        }
      }
      return { hasCompletedQuiz: false }
    }
  }
}
</script>

<style scoped>
.chatbot-container {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 1000;
}

.chatbot-toggle-btn {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  position: fixed;
  bottom: 24px;
  right: 24px;
}

.chatbot-window {
  position: fixed;
  bottom: 24px;
  right: 24px;
  display: flex;
  flex-direction: column;
  border-radius: 12px;
  overflow: hidden;
}

.chatbot-header {
  background: linear-gradient(135deg, #1565C0 0%, #0D47A1 100%);
  color: white;
  padding: 16px;
}

.chatbot-messages {
  flex: 1;
  overflow-y: auto;
  background-color: #f5f5f5;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.message {
  display: flex;
  width: 100%;
}

.message.user {
  justify-content: flex-end;
}

.message.bot {
  justify-content: flex-start;
}

.message-content {
  max-width: 75%;
  display: flex;
  flex-direction: column;
}

.message.user .message-content {
  align-items: flex-end;
}

.message.bot .message-content {
  align-items: flex-start;
}

.message-bubble {
  padding: 12px 16px;
  border-radius: 18px;
  word-wrap: break-word;
  line-height: 1.4;
}

.user-bubble {
  background-color: #1565C0;
  color: white;
  border-bottom-right-radius: 4px;
}

.bot-bubble {
  background-color: white;
  color: #212121;
  border: 1px solid #e0e0e0;
  border-bottom-left-radius: 4px;
}

/* Markdown styling inside bot messages */
.bot-bubble :deep(strong) {
  font-weight: 600;
  color: #1565C0;
}

.bot-bubble :deep(em) {
  font-style: italic;
}

.bot-bubble :deep(.chat-list) {
  margin: 8px 0;
  padding-left: 20px;
}

.bot-bubble :deep(.chat-list li) {
  margin: 4px 0;
  line-height: 1.5;
}

.bot-bubble :deep(ol.chat-list) {
  list-style-type: decimal;
}

.bot-bubble :deep(ul.chat-list) {
  list-style-type: disc;
}

.bot-bubble :deep(.code-block) {
  background-color: #f5f5f5;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  padding: 8px 12px;
  margin: 8px 0;
  font-family: 'Courier New', monospace;
  font-size: 0.85em;
  overflow-x: auto;
  white-space: pre-wrap;
}

.bot-bubble :deep(.inline-code) {
  background-color: #f0f0f0;
  border-radius: 3px;
  padding: 2px 6px;
  font-family: 'Courier New', monospace;
  font-size: 0.9em;
}

.message-time {
  font-size: 10px;
  color: #757575;
  margin-top: 4px;
  padding: 0 4px;
}

.quick-replies {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.chatbot-input {
  background-color: white;
  border-top: 1px solid #e0e0e0;
}

.welcome-section {
  background: linear-gradient(180deg, #e3f2fd 0%, #f5f5f5 100%);
}

.starter-questions {
  background: white;
  border-radius: 12px;
  padding: 12px;
  border: 1px solid #e0e0e0;
}

/* Scrollbar styling */
.chatbot-messages::-webkit-scrollbar {
  width: 6px;
}

.chatbot-messages::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.chatbot-messages::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 3px;
}

.chatbot-messages::-webkit-scrollbar-thumb:hover {
  background: #555;
}

/* Responsive */
@media (max-width: 600px) {
  .chatbot-window {
    width: calc(100vw - 48px);
    height: calc(100vh - 120px);
    max-width: 400px;
    max-height: 600px;
  }
  
  .chatbot-toggle-btn {
    bottom: 16px;
    right: 16px;
  }
  
  .chatbot-window {
    bottom: 16px;
    right: 16px;
  }
}
</style>
