import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Profile from '../views/Profile.vue'
import CareerTest from '../views/CareerTest.vue'
import Results from '../views/Results.vue'
import About from '../views/About.vue'
import FAQ from '../views/FAQ.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import { auth } from '../store/auth'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile
  },
  {
    path: '/career-test',
    name: 'CareerTest',
    component: CareerTest,
    meta: { requiresAuth: true }
  },
  {
    path: '/results',
    name: 'Results',
    component: Results
  },
  {
    path: '/about',
    name: 'About',
    component: About
  },
  {
    path: '/faq',
    name: 'FAQ',
    component: FAQ
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard for authentication
router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !auth.isLoggedIn) {
    // Store the intended destination
    sessionStorage.setItem('redirectAfterLogin', to.fullPath)
    // Trigger login dialog by going to a special route
    next({ name: 'Home', query: { showLogin: 'true' } })
  } else {
    next()
  }
})

export default router
