// Chatbot service - calls backend API which handles Gemini
import { API_URL } from '../config/api'

/**
 * Sends a message to the chatbot via the backend API
 */
export async function sendMessage(userMessage, context = {}) {
  try {
    const response = await fetch(`${API_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message: userMessage,
        context: context
      })
    })
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(`API error: ${response.status} - ${errorData.message || response.statusText}`)
    }
    
    const data = await response.json()
    
    if (!data.success) {
      throw new Error(data.message || 'Failed to get chatbot response')
    }
    
    return data.response
  } catch (error) {
    console.error('Chatbot API error:', error)
    
    // Return error response
    const userLang = context?.user?.lang || 'en'
    const errorMessage = userLang === 'vi' 
      ? 'Xin lỗi, đã xảy ra lỗi khi xử lý yêu cầu của bạn. Vui lòng thử lại sau.'
      : 'Sorry, an error occurred while processing your request. Please try again later.'
    
    return {
      reply: errorMessage,
      action: null,
      quickReplies: [],
      metadata: { confidence: 0, error: error.message }
    }
  }
}

/**
 * Builds context object from current app state
 */
export function buildContext(user, currentPage, testState = null, latestResultSummary = null) {
  return {
    sessionId: `session-${Date.now()}`,
    user: user ? {
      id: user.id,
      name: user.username || user.name,
      lang: user.lang || 'en',
      auth: !!user
    } : null,
    currentPage: currentPage || 'Home',
    testState: testState || null,
    latestResultSummary: latestResultSummary || null
  }
}
