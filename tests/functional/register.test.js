import { mount } from '@vue/test-utils'
import { describe, it, expect, vi } from 'vitest'
import Register from '../../src/views/Register.vue'
import { auth } from '../../src/store/auth'
import { API_URL } from '../../src/config/api'

const fetchMock = vi.fn()
globalThis.fetch = fetchMock

describe('Register View Functional', () => {
  it('should register user and redirect', async () => {
    const pushMock = vi.fn()
    const wrapper = mount(Register, {
      global: {
        stubs: {
          'v-container': { template: '<div><slot /></div>' },
          'v-row': { template: '<div><slot /></div>' },
          'v-col': { template: '<div><slot /></div>' },
          'v-card': { template: '<div><slot /></div>' },
          'v-toolbar': { template: '<div><slot /></div>' },
          'v-toolbar-title': { template: '<div><slot /></div>' },
          'v-card-text': { template: '<div><slot /></div>' },
          'v-form': { 
            template: '<form ref="form" @submit.prevent="$emit(\'submit\', $event)"><slot /></form>',
            methods: {
              validate: () => Promise.resolve({ valid: true })
            }
          },
          'v-text-field': {
            template: '<input :value="modelValue" @input="$emit(\'update:modelValue\', $event.target.value)" />',
            props: ['modelValue']
          },
          'v-select': {
             template: '<select :value="modelValue" @change="$emit(\'update:modelValue\', $event.target.value)"><option value="Department of Computer Science and Engineering">CS</option></select>',
             props: ['modelValue', 'items']
          },
          'v-btn': {
            template: '<button type="submit"><slot /></button>'
          },
          'router-link': { template: '<a><slot /></a>' },
          'v-snackbar': { template: '<div><slot /></div>' },
          'v-radio-group': { template: '<div><slot /></div>' },
          'v-radio': { template: '<div></div>' },
          'v-checkbox': { 
            template: '<input type="checkbox" :checked="modelValue" @change="$emit(\'update:modelValue\', $event.target.checked)" />',
            props: ['modelValue']
          }
        },
        mocks: {
          $router: { push: pushMock }
        }
      }
    })

    fetchMock.mockResolvedValueOnce({
      json: () => Promise.resolve({ success: true, user: { username: 'newuser' }, accessToken: 'access-token', refreshToken: 'refresh-token' })
    })

    const inputs = wrapper.findAll('input')
    await inputs[0].setValue('newuser')
    await inputs[1].setValue('password')
    
    const select = wrapper.find('select')
    await select.setValue('Department of Computer Science and Engineering')

    await wrapper.find('form').trigger('submit')

    expect(fetchMock).toHaveBeenCalledWith(`${API_URL}/register`, expect.any(Object))
    
    await new Promise(r => setTimeout(r, 1100)) // Wait for timeout in component
    expect(auth.isLoggedIn).toBe(true)
    expect(pushMock).toHaveBeenCalledWith({ name: 'Home' })
  })
})
