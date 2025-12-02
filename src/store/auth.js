import { reactive } from 'vue'
import { API_URL } from '../config/api'

export const auth = reactive({
  isLoggedIn: false,
  user: null,
  accessToken: null,
  refreshToken: null,

  init() {
    // Load tokens from localStorage on app start
    const accessToken = localStorage.getItem('accessToken')
    const refreshToken = localStorage.getItem('refreshToken')
    const user = localStorage.getItem('user')

    if (accessToken && refreshToken && user) {
      this.accessToken = accessToken
      this.refreshToken = refreshToken
      this.user = JSON.parse(user)
      this.isLoggedIn = true
    }
  },

  login(user, accessToken, refreshToken) {
    this.isLoggedIn = true
    this.user = user
    this.accessToken = accessToken
    this.refreshToken = refreshToken

    // Store in localStorage
    localStorage.setItem('accessToken', accessToken)
    localStorage.setItem('refreshToken', refreshToken)
    localStorage.setItem('user', JSON.stringify(user))
  },

  async logout() {
    // Call logout endpoint to invalidate refresh token
    if (this.refreshToken) {
      try {
        await fetch(`${API_URL}/logout`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ refreshToken: this.refreshToken })
        })
      } catch (error) {
        console.error('Logout error:', error)
      }
    }

    this.isLoggedIn = false
    this.user = null
    this.accessToken = null
    this.refreshToken = null

    localStorage.removeItem('accessToken')
    localStorage.removeItem('refreshToken')
    localStorage.removeItem('user')
  },

  async refreshAccessToken() {
    if (!this.refreshToken) {
      this.logout()
      return null
    }

    try {
      const response = await fetch(`${API_URL}/refresh`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refreshToken: this.refreshToken })
      })

      const data = await response.json()

      if (data.success && data.accessToken) {
        this.accessToken = data.accessToken
        localStorage.setItem('accessToken', data.accessToken)
        return data.accessToken
      } else {
        this.logout()
        return null
      }
    } catch (error) {
      console.error('Token refresh error:', error)
      this.logout()
      return null
    }
  },

  getAuthHeader() {
    return this.accessToken ? `Bearer ${this.accessToken}` : null
  }
})

// Initialize auth on module load
auth.init()
