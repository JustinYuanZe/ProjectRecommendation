import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import Results from '../../src/views/Results.vue'
import { auth } from '../../src/store/auth'
import { API_URL } from '../../src/config/api'

const fetchMock = vi.fn()
globalThis.fetch = fetchMock

describe('Results - Database Loading', () => {
  beforeEach(() => {
    fetchMock.mockClear()
    auth.logout()
    localStorage.clear()
  })

  it('should load results from database when user is logged in', async () => {
    auth.login({ id: 1, username: 'testuser' })

    const mockResults = {
      topRecommendations: [
        {
          field: 'technology',
          score: 5,
          title: 'Information Technology',
          careers: ['Programmer', 'Software Engineer'],
          description: 'Tech careers'
        }
      ],
      answerSummary: { technical: 3 }
    }

    fetchMock.mockResolvedValueOnce({
      json: () => Promise.resolve({
        success: true,
        results: [
          {
            id: 1,
            userId: 1,
            results: mockResults,
            completedAt: '2025-01-01'
          }
        ]
      })
    })

    const wrapper = mount(Results, {
      global: {
        stubs: {
          'v-container': { template: '<div><slot /></div>' },
          'v-row': { template: '<div><slot /></div>' },
          'v-col': { template: '<div><slot /></div>' },
          'v-card': { template: '<div><slot /></div>' },
          'v-card-title': { template: '<div><slot /></div>' },
          'v-card-text': { template: '<div><slot /></div>' },
          'v-card-actions': { template: '<div><slot /></div>' },
          'v-expansion-panels': { template: '<div><slot /></div>' },
          'v-expansion-panel': { template: '<div><slot /></div>' },
          'v-expansion-panel-title': { template: '<div><slot /></div>' },
          'v-expansion-panel-text': { template: '<div><slot /></div>' },
          'v-chip': { template: '<span><slot /></span>' },
          'v-chip-group': { template: '<div><slot /></div>' },
          'v-progress-linear': { template: '<div></div>' },
          'v-alert': { template: '<div><slot /></div>' },
          'v-list': { template: '<div><slot /></div>' },
          'v-list-item': { template: '<div><slot /></div>' },
          'v-list-item-title': { template: '<div><slot /></div>' },
          'v-btn': { template: '<button><slot /></button>' },
          'v-icon': { template: '<span></span>' }
        }
      }
    })

    await wrapper.vm.$nextTick()
    await new Promise(r => setTimeout(r, 50))

    expect(fetchMock).toHaveBeenCalledWith(`${API_URL}/test-results/1`)
    expect(wrapper.vm.results).toEqual(mockResults)
  })

  it('should fallback to localStorage when database fetch fails', async () => {
    auth.login({ id: 1, username: 'testuser' })

    const localResults = {
      topRecommendations: [{ field: 'business', score: 3 }]
    }
    localStorage.setItem('careerResults', JSON.stringify(localResults))

    fetchMock.mockRejectedValueOnce(new Error('Network error'))

    const wrapper = mount(Results, {
      global: {
        stubs: {
          'v-container': { template: '<div><slot /></div>' },
          'v-row': { template: '<div><slot /></div>' },
          'v-col': { template: '<div><slot /></div>' },
          'v-card': { template: '<div><slot /></div>' },
          'v-card-title': { template: '<div><slot /></div>' },
          'v-card-text': { template: '<div><slot /></div>' },
          'v-card-actions': { template: '<div><slot /></div>' },
          'v-btn': { template: '<button><slot /></button>' },
          'v-icon': { template: '<span></span>' }
        }
      }
    })

    await wrapper.vm.$nextTick()
    await new Promise(r => setTimeout(r, 50))

    expect(wrapper.vm.results).toEqual(localResults)
  })
})
