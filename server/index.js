import app from './src/index.js'
import connectDB from './src/config/database.js'

const PORT = process.env.PORT || 3000

async function start() {
  try {
    // Connect to MongoDB
    await connectDB()
    
    // Start the server
    app.listen(PORT)
    
    console.log(`🐹 Elysia is running at http://localhost:${PORT}`)
  } catch (error) {
    console.error('Failed to start server:', error)
    process.exit(1)
  }
}

start()
