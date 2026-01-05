import { describe, it, expect, beforeEach } from 'vitest'
import { createRouter, createMemoryHistory } from 'vue-router'
import { auth } from '../../src/store/auth'
import Home from '../../src/views/Home.vue'
import CareerTest from '../../src/views/CareerTest.vue'
import Login from '../../src/views/Login.vue'

describe('Router - Authentication Guard', () => {
  let router

  beforeEach(() => {
    auth.logout()
    sessionStorage.clear()
    
    router = createRouter({
      history: createMemoryHistory(),
      routes: [
        { path: '/', name: 'Home', component: Home },
        { 
          path: '/career-test', 
          name: 'CareerTest', 
          component: CareerTest,
          meta: { requiresAuth: true }
        },
        { path: '/login', name: 'Login', component: Login }
      ]
    })

    // Add navigation guard
    router.beforeEach((to, from, next) => {
      if (to.meta.requiresAuth && !auth.isLoggedIn) {
        sessionStorage.setItem('redirectAfterLogin', to.fullPath)
        next({ name: 'Home', query: { showLogin: 'true' } })
      } else {
        next()
      }
    })
  })

  it('should redirect to Home with showLogin query when accessing CareerTest without auth', async () => {
    await router.push('/career-test')
    
    expect(router.currentRoute.value.name).toBe('Home')
    expect(router.currentRoute.value.query.showLogin).toBe('true')
    expect(sessionStorage.getItem('redirectAfterLogin')).toBe('/career-test')
  })

  it('should allow access to CareerTest when authenticated', async () => {
    auth.login({ id: 1, username: 'testuser' })
    
    await router.push('/career-test')
    
    expect(router.currentRoute.value.name).toBe('CareerTest')
  })

  it('should allow access to Home without authentication', async () => {
    await router.push('/')
    
    expect(router.currentRoute.value.name).toBe('Home')
  })
})
