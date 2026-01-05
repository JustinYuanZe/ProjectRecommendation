import { mount } from '@vue/test-utils'
import { describe, it, expect, vi } from 'vitest'
import Home from '../../src/views/Home.vue'
import { auth } from '../../src/store/auth'

describe('E2E Flow Simulation', () => {
  it('should show login modal when clicking start test without login', async () => {
    auth.logout()
    const pushMock = vi.fn()
    const wrapper = mount(Home, {
      global: {
        stubs: {
          'v-container': { template: '<div><slot /></div>' },
          'v-row': { template: '<div><slot /></div>' },
          'v-col': { template: '<div><slot /></div>' },
          'v-card': { template: '<div><slot /></div>' },
          'v-card-item': { template: '<div><slot /></div>' },
          'v-card-title': { template: '<div><slot /></div>' },
          'v-card-subtitle': { template: '<div><slot /></div>' },
          'v-card-actions': { template: '<div><slot /></div>' },
          'v-spacer': { template: '<div></div>' },
          'v-icon': { template: '<span><slot /></span>' },
          'v-img': { template: '<img />' },
          'v-btn': {
            template: '<button @click="$emit(\'click\')"><slot /></button>'
          },
          'v-dialog': {
            template: '<div v-if="modelValue" class="dialog"><slot /></div>',
            props: ['modelValue']
          },
          'v-card-text': { template: '<div><slot /></div>' },
          'router-link': { template: '<a><slot /></a>' },
          'v-alert': { template: '<div><slot /></div>' }
        },
        mocks: {
          $router: { push: pushMock, replace: vi.fn() },
          $route: { query: {} }
        }
      }
    })

    const buttons = wrapper.findAll('button')
    const startTestBtn = buttons.find(b => b.text().includes('Start Assessment'))
    
    if (startTestBtn) {
      await startTestBtn.trigger('click')
      expect(wrapper.find('.dialog').exists()).toBe(true)
      expect(wrapper.find('.dialog').text()).toContain('Authentication Required')
    } else {
      throw new Error('Start Test button not found')
    }
  })
})
