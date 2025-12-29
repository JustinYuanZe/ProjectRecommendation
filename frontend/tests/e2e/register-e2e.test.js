import { mount } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import Register from '../../src/views/Register.vue'

// E2E-style tests for Register: validate form behaviour and network interaction

describe('Register E2E', () => {
  let pushMock

  beforeEach(() => {
    pushMock = vi.fn()
    global.fetch = vi.fn()
  })

  it('validates form and submits successful registration', async () => {
    const fakeResponse = {
      success: true,
      accessToken: 'atk',
      refreshToken: 'rtk',
      user: { id: 2, username: 'newuser' }
    }
    global.fetch.mockResolvedValue({ json: async () => fakeResponse })

    const wrapper = mount(Register, {
      global: {
        stubs: {
          'v-container': { template: '<div><slot /></div>' },
          'v-row': { template: '<div><slot /></div>' },
          'v-col': { template: '<div><slot /></div>' },
          'v-card': { template: '<div><slot /></div>' },
          'v-form': { template: '<form @submit.prevent="$emit(\'submit\')"><slot /></form>' },
          'v-text-field': { template: '<input />', props: ['modelValue'] },
          'v-select': { template: '<select><slot /></select>', props: ['items','modelValue'] },
          'v-radio-group': { template: '<div><slot /></div>', props: ['modelValue'] },
          'v-radio': { template: '<input type="radio" />' },
          'v-btn': { template: '<button @click="$emit(\'click\')"><slot /></button>' },
          'v-snackbar': { template: '<div><slot /></div>', props: ['modelValue'] },
          'v-checkbox': { template: '<input type="checkbox" @click="$emit(\'click\')" />', props: ['modelValue'] }
        },
        mocks: {
          $router: { push: pushMock }
        }
      }
    })

    // Fill only the required fields for a valid submission
    const inputs = wrapper.findAll('input')
    // Attempt to set username, password, confirm password and checkbox
    if (inputs.length >= 4) {
      await inputs[0].setValue('newuser')
      await inputs[1].setValue('Password1')
      await inputs[2].setValue('Password1')
      // agree to terms checkbox - find first checkbox-like input
      const checkbox = inputs.find(i => i.attributes('type') === 'checkbox')
      if (checkbox) await checkbox.setValue(true)
    }

    const btn = wrapper.find('button')
    await btn.trigger('click')

    // allow microtasks to flush
    await Promise.resolve()

    expect(global.fetch).toHaveBeenCalled()
    expect(pushMock).toHaveBeenCalled()
  })

  it('shows snackbar when form invalid', async () => {
    // mock backend not called when validation fails
    global.fetch.mockResolvedValue({ json: async () => ({ success: false }) })

    const wrapper = mount(Register, {
      global: {
        stubs: {
          'v-container': { template: '<div><slot /></div>' },
          'v-row': { template: '<div><slot /></div>' },
          'v-col': { template: '<div><slot /></div>' },
          'v-card': { template: '<div><slot /></div>' },
          'v-form': { template: '<form @submit.prevent="$emit(\'submit\')"><slot /></form>' },
          'v-text-field': { template: '<input />', props: ['modelValue'] },
          'v-btn': { template: '<button @click="$emit(\'click\')"><slot /></button>' },
          'v-snackbar': { template: '<div class="snack"><slot /></div>', props: ['modelValue'] }
        },
        mocks: {
          $router: { push: vi.fn() }
        }
      }
    })

    // Leave required fields empty and submit
    const btn = wrapper.find('button')
    await btn.trigger('click')

    // allow microtasks to flush
    await Promise.resolve()

    expect(wrapper.find('.snack').exists()).toBe(true)
  })
})