<template>
  <div class="chatbot-container">
    <!-- Floating Button -->
    <v-btn
      v-if="!isOpen"
      class="chatbot-toggle-btn"
      color="primary"
      size="default"
      icon
      elevation="4"
      @click="toggleChat"
    >
      <v-icon size="22">mdi-chat</v-icon>
    </v-btn>

    <!-- Chat Window -->
    <v-card
      v-if="isOpen"
      class="chatbot-window"
      elevation="8"
      width="340"
      height="480"
    >
      <!-- Header -->
      <v-card-title class="chatbot-header d-flex align-center justify-space-between py-2 px-3">
        <div class="d-flex align-center">
          <v-icon color="white" size="small" class="mr-2">mdi-robot-happy</v-icon>
          <span class="text-white text-body-2 font-weight-bold">{{ $t('chatbot.title') }}</span>
        </div>
        <div>
          <v-btn
            icon
            variant="text"
            size="small"
            @click="clearChat"
            :title="$t('chatbot.clearChat')"
          >
            <v-icon color="white" size="small">mdi-delete-outline</v-icon>
          </v-btn>
          <v-btn
            icon
            variant="text"
            size="small"
            @click="toggleChat"
            :title="$t('common.close')"
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
            <h3 class="text-h6 mb-1">{{ $t('chatbot.welcome') }}</h3>
            <p class="text-body-2 text-grey">{{ $t('chatbot.welcomeDesc') }}</p>
          </div>
          <div class="starter-questions">
            <p class="text-caption text-grey-darken-1 mb-2">{{ $t('chatbot.tryAsking') }}</p>
            <v-chip
              v-for="(question, key) in translatedStarterQuestions"
              :key="key"
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
            <div v-else class="message-bubble bot-bubble" @click="handleLinkClick">
              <div v-html="formatMessage(message.text)"></div>
            </div>
            <!-- Quick replies outside the bubble for better visibility -->
            <div v-if="message.type === 'bot' && message.quickReplies && message.quickReplies.length > 0" class="quick-replies mt-2">
              <v-chip
                v-for="(reply, idx) in message.quickReplies"
                :key="idx"
                size="small"
                variant="outlined"
                color="primary"
                class="mr-1 mb-1"
                @click="handleQuickReply(reply)"
                style="cursor: pointer;"
              >
                {{ reply }}
              </v-chip>
            </div>
            <div class="message-time">{{ formatTime(message.timestamp) }}</div>
          </div>
        </div>

        <div v-if="loading" class="message bot">
          <div class="message-content">
            <div class="message-bubble bot-bubble">
              <v-progress-circular indeterminate size="20" color="primary"></v-progress-circular>
              <span class="ml-2">{{ $t('chatbot.thinking') }}</span>
            </div>
          </div>
        </div>
      </v-card-text>

      <!-- Input Area -->
      <v-card-actions class="chatbot-input pa-2">
        <v-text-field
          v-model="inputMessage"
          :placeholder="$t('chatbot.placeholder')"
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
      loading: false
    }
  },
  computed: {
    translatedStarterQuestions() {
      return [
        this.$t('chatbot.starterQuestions.q1'),
        this.$t('chatbot.starterQuestions.q2'),
        this.$t('chatbot.starterQuestions.q3'),
        this.$t('chatbot.starterQuestions.q4'),
        this.$t('chatbot.starterQuestions.q5')
      ]
    },
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
    // Load chat history from sessionStorage
    const savedMessages = sessionStorage.getItem('chatbotMessages')
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
        // Scroll to bottom when opening chatbot
        this.$nextTick(() => {
          this.scrollToBottom()
        })
      }
    },
    messages: {
      handler() {
        // Save messages to sessionStorage
        sessionStorage.setItem('chatbotMessages', JSON.stringify(this.messages))
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
      sessionStorage.removeItem('chatbotMessages')
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
          latestResultSummary,
          this.$i18n.locale
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
          text: this.$t('chatbot.errorMessage'),
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
    
    handleLinkClick(event) {
      // Check if clicked element is a link
      const target = event.target
      if (target.tagName === 'A' && target.classList.contains('internal-link')) {
        event.preventDefault()
        const route = target.getAttribute('data-route')
        if (route) {
          this.$router.push(route)
          // Optionally close the chatbot after navigation
          // this.isOpen = false
        }
      }
    },
    
    formatMessage(text) {
      if (!text) return ''
      
      let formatted = text
      
      // First, protect code blocks and inline code from other processing
      const codeBlocks = []
      const inlineCodes = []
      const links = []
      
      // Extract and store code blocks
      formatted = formatted.replace(/```([\s\S]*?)```/g, (match, code) => {
        codeBlocks.push(code)
        return `__CODEBLOCK_${codeBlocks.length - 1}__`
      })
      
      // Extract and store inline code
      formatted = formatted.replace(/`([^`]+)`/g, (match, code) => {
        inlineCodes.push(code)
        return `__INLINECODE_${inlineCodes.length - 1}__`
      })
      
      // Extract and store markdown links [text](url)
      formatted = formatted.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (match, text, url) => {
        links.push({ text, url })
        return `__LINK_${links.length - 1}__`
      })
      
      // Now escape HTML to prevent XSS (but our placeholders are safe)
      formatted = formatted
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
      
      // Process markdown formatting
      // Headings (### Heading)
      formatted = formatted.replace(/^#### (.+)$/gm, '<h4 class="chat-heading">$1</h4>')
      formatted = formatted.replace(/^### (.+)$/gm, '<h3 class="chat-heading">$1</h3>')
      formatted = formatted.replace(/^## (.+)$/gm, '<h2 class="chat-heading">$1</h2>')
      formatted = formatted.replace(/^# (.+)$/gm, '<h1 class="chat-heading">$1</h1>')
      
      // Bold (**text** or __text__)
      formatted = formatted.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
      formatted = formatted.replace(/__([^_]+)__/g, '<strong>$1</strong>')
      
      // Italic (*text* or _text_) - be careful not to match list markers
      formatted = formatted.replace(/(?<!\w)\*([^*\n]+)\*(?!\w)/g, '<em>$1</em>')
      formatted = formatted.replace(/(?<!\w)_([^_\n]+)_(?!\w)/g, '<em>$1</em>')
      
      // Process lines for lists
      const lines = formatted.split('\n')
      let inList = false
      let listType = null
      const processedLines = []
      
      for (let i = 0; i < lines.length; i++) {
        let line = lines[i].trim()
        
        // Numbered list (1. item, 2. item, etc.)
        const numberedMatch = line.match(/^(\d+)\.\s+(.+)$/)
        // Bullet list (- item or * item)
        const bulletMatch = line.match(/^[\*\-]\s+(.+)$/)
        
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
          // Add line (preserve empty lines as <br>)
          if (line.length > 0) {
            processedLines.push(line)
          } else if (processedLines.length > 0) {
            processedLines.push('<br>')
          }
        }
      }
      
      // Close any open list
      if (inList) {
        processedLines.push(listType === 'ol' ? '</ol>' : '</ul>')
      }
      
      // Join processed lines
      formatted = processedLines.join('\n')
      
      // Replace newlines with proper spacing
      formatted = formatted.replace(/\n(?!<[ou]l|<li|<\/[ou]l|<br)/g, '<br>')
      formatted = formatted.replace(/\n/g, '')
      
      // Restore code blocks
      codeBlocks.forEach((code, i) => {
        // Decode HTML entities in code
        const decodedCode = code
          .replace(/&lt;/g, '<')
          .replace(/&gt;/g, '>')
          .replace(/&amp;/g, '&')
        formatted = formatted.replace(`__CODEBLOCK_${i}__`, `<pre class="code-block">${decodedCode}</pre>`)
      })
      
      // Restore inline code
      inlineCodes.forEach((code, i) => {
        const decodedCode = code
          .replace(/&lt;/g, '<')
          .replace(/&gt;/g, '>')
          .replace(/&amp;/g, '&')
        formatted = formatted.replace(`__INLINECODE_${i}__`, `<code class="inline-code">${decodedCode}</code>`)
      })
      
      // Restore markdown links as router-links or external links
      links.forEach((link, i) => {
        // Check if it's an internal route (starts with /)
        if (link.url.startsWith('/')) {
          // Internal route - make it clickable but don't use router-link in v-html
          formatted = formatted.replace(
            `__LINK_${i}__`, 
            `<a href="${link.url}" class="chat-link internal-link" data-route="${link.url}">${link.text}</a>`
          )
        } else {
          // External link
          formatted = formatted.replace(
            `__LINK_${i}__`, 
            `<a href="${link.url}" class="chat-link external-link" target="_blank" rel="noopener noreferrer">${link.text}</a>`
          )
        }
      })
      
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
        // Use requestAnimationFrame for smoother scrolling
        requestAnimationFrame(() => {
          container.scrollTop = container.scrollHeight
        })
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
  min-height: 44px;
}

.chatbot-messages {
  flex: 1;
  overflow-y: auto;
  background-color: #f5f5f5;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  scroll-behavior: smooth;
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

.bot-bubble :deep(.chat-heading) {
  font-weight: 600;
  color: #1565C0;
  margin: 8px 0 4px 0;
}

.bot-bubble :deep(h1.chat-heading) {
  font-size: 1.25em;
  margin-top: 12px;
}

.bot-bubble :deep(h2.chat-heading) {
  font-size: 1.15em;
  margin-top: 10px;
}

.bot-bubble :deep(h3.chat-heading) {
  font-size: 1.05em;
  margin-top: 8px;
}

.bot-bubble :deep(h4.chat-heading) {
  font-size: 1em;
  margin-top: 6px;
}

.bot-bubble :deep(.chat-link) {
  color: #1976d2;
  text-decoration: none;
  font-weight: 500;
  cursor: pointer;
  border-bottom: 1px solid #1976d2;
  transition: all 0.2s ease;
}

.bot-bubble :deep(.chat-link:hover) {
  color: #1565c0;
  border-bottom-color: #1565c0;
  background-color: rgba(25, 118, 210, 0.05);
}

.bot-bubble :deep(.external-link)::after {
  content: ' ↗';
  font-size: 0.85em;
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
  gap: 6px;
  margin-left: 4px;
}

.quick-replies .v-chip {
  transition: all 0.2s ease;
  font-size: 0.813rem;
}

.quick-replies .v-chip:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
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
    width: calc(100vw - 32px);
    height: calc(100vh - 100px);
    max-width: 360px;
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
