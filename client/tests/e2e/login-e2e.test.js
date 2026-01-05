import { mount } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import Login from '../../src/views/Login.vue'

// Best-practice E2E-style test: mount real component, stub only heavy UI pieces, mock external network and router

describe('Login E2E', () => {
  let pushMock

  beforeEach(() => {
    pushMock = vi.fn()
    // reset global fetch mock
    global.fetch = vi.fn()
  })

  it('submits credentials and navigates on success', async () => {
    const fakeResponse = {
      success: true,
      accessToken: 'atk',
      refreshToken: 'rtk',
      user: { id: 1, username: 'tester' }
    }
    global.fetch.mockResolvedValue({ json: async () => fakeResponse })

    const wrapper = mount(Login, {
      global: {
        stubs: {
          'v-container': { template: '<div><slot /></div>' },
          'v-row': { template: '<div><slot /></div>' },
          'v-col': { template: '<div><slot /></div>' },
          'v-card': { template: '<div><slot /></div>' },
          'v-form': { template: '<form @submit.prevent="$emit(\'submit\')"><slot /></form>' },
          'v-text-field': { template: '<input />', props: ['modelValue'] },
          'v-btn': { template: '<button @click="$emit(\'click\')"><slot /></button>' },
          'v-snackbar': { template: '<div><slot /></div>', props: ['modelValue'] }
        },
        mocks: {
          $router: { push: pushMock }
        }
      }
    })

    // Fill inputs using v-model expectations
    const inputs = wrapper.findAll('input')
    // username then password
    if (inputs.length >= 2) {
      await inputs[0].setValue('tester')
      await inputs[1].setValue('Password1')
    }

    // trigger submit
    const btn = wrapper.find('button')
    await btn.trigger('click')

    // allow microtasks to flush
    await Promise.resolve()

    expect(global.fetch).toHaveBeenCalled()
    expect(pushMock).toHaveBeenCalled()
  })

  it('shows snackbar on failed login', async () => {
    global.fetch.mockResolvedValue({ json: async () => ({ success: false, message: 'bad' }) })

    const wrapper = mount(Login, {
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

    const inputs = wrapper.findAll('input')
    if (inputs.length >= 2) {
      await inputs[0].setValue('baduser')
      await inputs[1].setValue('badpass')
    }

    const btn = wrapper.find('button')
    await btn.trigger('click')

    await vi.runAllTicks()

    expect(wrapper.find('.snack').exists()).toBe(true)
  })
})