import { describe, it, expect, beforeEach, vi } from 'vitest'
import { auth } from '../../src/store/auth'

// Mock fetch for logout
const fetchMock = vi.fn()
globalThis.fetch = fetchMock

describe('Auth Store', () => {
  beforeEach(async () => {
    fetchMock.mockResolvedValue({
      json: () => Promise.resolve({ success: true })
    })
    await auth.logout()
    fetchMock.mockClear()
  })

  it('should be initially logged out', () => {
    expect(auth.isLoggedIn).toBe(false)
    expect(auth.user).toBe(null)
  })

  it('should login user', () => {
    const user = { username: 'test', id: 1 }
    auth.login(user, 'access-token', 'refresh-token')
    expect(auth.isLoggedIn).toBe(true)
    expect(auth.user).toEqual(user)
  })

  it('should logout user', async () => {
    const user = { username: 'test', id: 1 }
    auth.login(user, 'access-token', 'refresh-token')
    fetchMock.mockResolvedValueOnce({
      json: () => Promise.resolve({ success: true })
    })
    await auth.logout()
    expect(auth.isLoggedIn).toBe(false)
    expect(auth.user).toBe(null)
  })
})
