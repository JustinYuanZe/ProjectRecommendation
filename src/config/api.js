// API Configuration
export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:3000'

// API Endpoints
export const API_ENDPOINTS = {
  BASE_URL: API_URL,
  LOGIN: `${API_URL}/login`,
  REGISTER: `${API_URL}/register`,
  REFRESH: `${API_URL}/refresh`,
  LOGOUT: `${API_URL}/logout`,
  TEST_RESULTS: `${API_URL}/test-results`,
  QUESTIONS: `${API_URL}/questions`,
  CHAT: `${API_URL}/chat`
}
