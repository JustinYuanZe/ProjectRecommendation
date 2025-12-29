import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import CareerTest from '../../src/views/CareerTest.vue'
import { auth } from '../../src/store/auth'
import { API_URL } from '../../src/config/api'

const fetchMock = vi.fn()
globalThis.fetch = fetchMock

describe('CareerTest - Database Storage', () => {
  beforeEach(() => {
    fetchMock.mockClear()
    auth.logout()
    localStorage.clear()
  })

  it('should save test results to database when user is logged in', async () => {
    // Login user
    auth.login({ id: 1, username: 'testuser' })

    const wrapper = mount(CareerTest, {
      global: {
        stubs: {
          'v-container': { template: '<div><slot /></div>' },
          'v-row': { template: '<div><slot /></div>' },
          'v-col': { template: '<div><slot /></div>' },
          'v-card': { template: '<div><slot /></div>' },
          'v-card-title': { template: '<div><slot /></div>' },
          'v-card-subtitle': { template: '<div><slot /></div>' },
          'v-progress-linear': { template: '<div></div>' },
          'v-radio-group': {
            template: '<div><slot /></div>',
            props: ['modelValue']
          },
          'v-radio': { template: '<div></div>' },
          'v-card-actions': { template: '<div><slot /></div>' },
          'v-btn': {
            template: '<button @click="$emit(\'click\')"><slot /></button>'
          },
          'v-icon': { template: '<span></span>' }
        }
      }
    })

    // Simulate answering all questions
    wrapper.vm.answers = {
      0: 'technical',
      1: 'analytical',
      2: 'financial',
      3: 'data',
      4: 'technical',
      5: 'technology',
      6: 'structured',
      7: 'tech_learning'
    }

    // Mock successful API response
    fetchMock.mockResolvedValueOnce({
      json: () => Promise.resolve({ success: true, testResult: { id: 123 } })
    })

    // Finish test
    await wrapper.vm.finishTest()

    // Wait for async operations
    await new Promise(r => setTimeout(r, 50))

    // Verify API was called with correct data
    expect(fetchMock).toHaveBeenCalledWith(
      `${API_URL}/test-results`,
      expect.objectContaining({
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: expect.stringContaining('"userId":1')
      })
    )
  })

  it('should not call API when user is not logged in', async () => {
    const wrapper = mount(CareerTest, {
      global: {
        stubs: {
          'v-container': { template: '<div><slot /></div>' },
          'v-row': { template: '<div><slot /></div>' },
          'v-col': { template: '<div><slot /></div>' },
          'v-card': { template: '<div><slot /></div>' },
          'v-card-title': { template: '<div><slot /></div>' },
          'v-card-subtitle': { template: '<div><slot /></div>' },
          'v-progress-linear': { template: '<div></div>' },
          'v-radio-group': { template: '<div><slot /></div>' },
          'v-radio': { template: '<div></div>' },
          'v-card-actions': { template: '<div><slot /></div>' },
          'v-btn': { template: '<button><slot /></button>' },
          'v-icon': { template: '<span></span>' }
        }
      }
    })

    wrapper.vm.answers = { 0: 'test' }
    await wrapper.vm.finishTest()
    await new Promise(r => setTimeout(r, 50))

    // Should not call API
    expect(fetchMock).not.toHaveBeenCalled()
    
    // But should still save to localStorage
    expect(localStorage.getItem('careerResults')).toBeTruthy()
  })
})
