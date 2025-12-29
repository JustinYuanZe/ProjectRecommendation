export const API_URL = import.meta.env.VITE_API_URL || "http://localhost:3000";

export const PYTHON_API_URL = "https://justinyz-career-advisor-api.hf.space";

export const API_ENDPOINTS = {
  BASE_URL: API_URL,
  
  LOGIN: `${API_URL}/api/login`,
  REGISTER: `${API_URL}/api/register`,
  REFRESH: `${API_URL}/api/refresh`,
  LOGOUT: `${API_URL}/api/logout`,
  
  QUESTIONS: `${API_URL}/api/questions`,
  TEST_RESULTS: `${API_URL}/api/test-results`,
  TEST_RESULTS_BY_USER: (userId) => `${API_URL}/api/test-results/${userId}`,
  
  USER_PROFILE: (userId) => `${API_URL}/api/users/${userId}/profile`,
  
  CHATBOT: `${API_URL}/api/chatbot/message`,
  
  CAREER_ANALYSIS: `${API_URL}/api/analyze-career`
}