// Chatbot service - Backend API integration with Gemini AI
import { API_ENDPOINTS } from '../config/api'

/**
 * Generate quick replies based on user message and context
 */
function generateQuickReplies(userMessage, context) {
  const lowerMsg = userMessage.toLowerCase()
  const results = context?.latestResultSummary
  
  // Career/job related queries
  if (lowerMsg.includes('career') || lowerMsg.includes('job') || lowerMsg.includes('result')) {
    if (results?.hasCompletedQuiz) {
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
  if (results?.hasCompletedQuiz) {
    return ['Explain my results', 'Career advice', 'Next steps']
  }
  return ['Take career quiz', 'How does the quiz work?', 'Career options']
}

/**
 * Sends a message to the backend chatbot API
 */
export async function sendMessage(userMessage, context = {}) {
  try {
    const response = await fetch(API_ENDPOINTS.CHATBOT, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        message: userMessage,
        context: context
      })
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()

    // If backend returns an error but with a reply, use it
    if (data.error && data.reply) {
      return {
        reply: data.reply,
        action: data.action || null,
        quickReplies: data.quickReplies || generateQuickReplies(userMessage, context),
        metadata: data.metadata || { confidence: 0, error: data.error }
      }
    }

    // Normal successful response
    return {
      reply: data.reply || 'I apologize, but I couldn\'t generate a response. Please try again.',
      action: data.action || null,
      quickReplies: data.quickReplies || generateQuickReplies(userMessage, context),
      metadata: data.metadata || { confidence: 0.8 }
    }

  } catch (error) {
    console.error('Chatbot API error:', error)
    
    // Return error response
    const userLang = context?.user?.lang || 'en'
    let errorMessage = 'Sorry, an error occurred while connecting to the chatbot. Please try again later.'
    
    if (userLang === 'zh-TW') {
      errorMessage = '抱歉，連接聊天機器人時發生錯誤，請稍後再試。'
    } else if (userLang === 'vi') {
      errorMessage = 'Xin lỗi, đã xảy ra lỗi khi kết nối với chatbot. Vui lòng thử lại sau.'
    }
    
    return {
      reply: errorMessage,
      action: null,
      quickReplies: generateQuickReplies(userMessage, context),
      metadata: { confidence: 0, error: error.message }
    }
  }
}

/**
 * Builds context object from current app state
 */
export function buildContext(user, currentPage, testState = null, latestResultSummary = null, locale = 'en') {
  // Map locale to lang code for chatbot
  const langMap = {
    'en': 'en',
    'zh-TW': 'zh-TW',
    'vi': 'vi'
  }
  const lang = langMap[locale] || 'en'
  
  return {
    sessionId: `session-${Date.now()}`,
    user: user ? {
      id: user.id,
      name: user.username || user.name,
      lang: lang,
      auth: !!user
    } : {
      lang: lang
    },
    currentPage: currentPage || 'Home',
    testState: testState || null,
    latestResultSummary: latestResultSummary || null
  }
}
