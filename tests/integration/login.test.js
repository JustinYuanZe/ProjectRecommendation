import { mount } from '@vue/test-utils'
import { describe, it, expect, vi } from 'vitest'
import Login from '../../src/views/Login.vue'
import { auth } from '../../src/store/auth'
import { API_URL } from '../../src/config/api'

const fetchMock = vi.fn()
globalThis.fetch = fetchMock

describe('Login View Integration', () => {
  it('should call login API and update store on success', async () => {
    const wrapper = mount(Login, {
      global: {
        stubs: {
          'v-container': { template: '<div><slot /></div>' },
          'v-row': { template: '<div><slot /></div>' },
          'v-col': { template: '<div><slot /></div>' },
          'v-card': { template: '<div><slot /></div>' },
          'v-toolbar': { template: '<div><slot /></div>' },
          'v-toolbar-title': { template: '<div><slot /></div>' },
          'v-card-text': { template: '<div><slot /></div>' },
          'v-form': { template: '<form @submit.prevent="$emit(\'submit\', $event)"><slot /></form>' },
          'v-text-field': {
            template: '<input :value="modelValue" @input="$emit(\'update:modelValue\', $event.target.value)" />',
            props: ['modelValue', 'label', 'type']
          },
          'v-btn': {
            template: '<button type="submit"><slot /></button>'
          },
          'router-link': { template: '<a><slot /></a>' },
          'v-snackbar': { template: '<div><slot /></div>' }
        },
        mocks: {
          $router: { push: vi.fn() }
        }
      }
    })

    // Mock successful API response
    fetchMock.mockResolvedValueOnce({
      json: () => Promise.resolve({ success: true, user: { username: 'test' }, accessToken: 'access-token', refreshToken: 'refresh-token' })
    })

    // Set input values
    const inputs = wrapper.findAll('input')
    await inputs[0].setValue('testuser')
    await inputs[1].setValue('password')

    // Trigger login
    await wrapper.find('form').trigger('submit')

    // Check fetch called
    expect(fetchMock).toHaveBeenCalledWith(`${API_URL}/login`, expect.any(Object))

    // Check auth store updated
    // We need to wait for the async handleLogin to finish
    await new Promise(r => setTimeout(r, 10))
    expect(auth.isLoggedIn).toBe(true)
    expect(auth.user.username).toBe('test')
  })
})
