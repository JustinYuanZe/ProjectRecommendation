import { Elysia } from 'elysia'
import { cors } from '@elysiajs/cors'
import { jwt } from '@elysiajs/jwt'
import connectDB from './config/database.js'
import { authRoutes, testRoutes, userRoutes, questionRoutes, chatbotRoutes } from './routes/index.js'

// JWT Secrets from environment
const ACCESS_TOKEN_SECRET = process.env.ACCESS_TOKEN_SECRET || 'your-access-token-secret-key-change-in-production'
const REFRESH_TOKEN_SECRET = process.env.REFRESH_TOKEN_SECRET || 'your-refresh-token-secret-key-change-in-production'

// Warn if using default secrets
if (ACCESS_TOKEN_SECRET === 'your-access-token-secret-key-change-in-production') {
  console.warn('⚠️  WARNING: Using default ACCESS_TOKEN_SECRET. Set a secure secret in production!')
}
if (REFRESH_TOKEN_SECRET === 'your-refresh-token-secret-key-change-in-production') {
  console.warn('⚠️  WARNING: Using default REFRESH_TOKEN_SECRET. Set a secure secret in production!')
}

// Create Elysia app
const app = new Elysia()
  .use(cors({
    origin: true,
    credentials: true,
    allowedHeaders: ['Content-Type', 'Authorization'],
    methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
  }))
  .use(
    jwt({
      name: 'jwt',
      secret: ACCESS_TOKEN_SECRET
    })
  )
  .use(
    jwt({
      name: 'refreshJwt',
      secret: REFRESH_TOKEN_SECRET
    })
  )
  // Middleware to ensure DB   connection before each request
  .onBeforeHandle(async () => {
    await connectDB()
  })
  .get('/', () => ({ 
    status: 'online',
    message: 'Job Quiz API Server',
    version: '1.0.0',
    timestamp: new Date().toISOString(),
    endpoints: {
      health: '/health',
      auth: '/api/login, /api/register, /api/refresh, /api/logout',
      test: '/api/test-results',
      user: '/api/users',
      questions: '/api/questions',
      chatbot: '/api/chatbot'
    }
  }))
  // Health check endpoint
  .get('/health', () => ({ 
    status: 'ok', 
    timestamp: new Date().toISOString(),
    database: 'connected',
    uptime: process.uptime()
  }))
  // Mount routes
  .group('/api', (app) => 
    app
      .use(authRoutes)
      .use(testRoutes)
      .use(userRoutes)
      .use(questionRoutes)
      .use(chatbotRoutes)
  )

// Export the Elysia app as default (required for Vercel)
export default app

