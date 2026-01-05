import { Elysia } from 'elysia'
import mongoose from 'mongoose'
import { TestResult, User } from '../models/index.js'
import { verifyToken } from '../middleware/auth.js'

const PYTHON_API_URL = "https://justinyz-career-advisor-api.hf.space";

export const testRoutes = new Elysia()
  .post('/test-results', async ({ body, set, request, jwt }) => {
    // Verify JWT token
    const authUser = await verifyToken(jwt, request)
    
    if (!authUser) {
      set.status = 401
      return { success: false, message: 'Unauthorized' }
    }

    const { userId, answers, results } = body

    if (!userId || !answers || !results) {
      set.status = 400
      return { success: false, message: 'Missing fields' }
    }

    // Verify userId matches token
    if (userId !== authUser.userId) {
      set.status = 403
      return { success: false, message: 'Forbidden' }
    }

    try {
      // Convert string userId to ObjectId
      const userIdObjectId = new mongoose.Types.ObjectId(authUser.userId)
      
      const testResult = new TestResult({
        userId: userIdObjectId,
        answers: new Map(Object.entries(answers)),
        results: {
          topRecommendations: results.topRecommendations || [],
          categoryScores: results.categoryScores || {}
        },
        completedAt: new Date()
      })

      await testResult.save()

      // Convert Map back to object for response
      const responseResult = {
        id: testResult._id,
        userId: testResult.userId,
        answers: Object.fromEntries(testResult.answers),
        results: testResult.results,
        completedAt: testResult.completedAt
      }

      return { success: true, testResult: responseResult }
    } catch (error) {
      console.error('Save test result error:', error)
      set.status = 500
      return { success: false, message: 'Internal server error' }
    }
  })

  .post('/analyze-career', async ({ body, set, request, jwt }) => {
    // Verify JWT token
    const authUser = await verifyToken(jwt, request)
    if (!authUser) {
      set.status = 401
      return { success: false, message: 'Unauthorized' }
    }

    const { answers } = body
    if (!answers) {
      set.status = 400
      return { success: false, message: 'Missing answers for analysis' }
    }

    try {
      // Forward to Python microservice
      const response = await fetch(`${PYTHON_API_URL}/api/analyze-career`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ answers })
      })

      if (!response.ok) {
        throw new Error('Python API failed')
      }

      const aiData = await response.json()

      // Save to user profile automatically
      const user = await User.findById(authUser.userId)
      if (user) {
        // Update only careerPath to avoid Mongoose casting issues with other profile fields
        user.profile.careerPath = {
          aiSummary: aiData.ai_summary,
          recommendedCourses: aiData.courses
        }
        await user.save()
      }

      return { 
        success: true, 
        ai_summary: aiData.ai_summary, 
        courses: aiData.courses,
        profile: user ? user.profile : null
      }
    } catch (error) {
      console.error('Analyze career error:', error)
      set.status = 500
      return { success: false, message: 'AI Analysis failed' }
    }
  })

  .get('/test-results/:userId', async ({ params, set, request, jwt }) => {
    // Verify JWT token
    const authUser = await verifyToken(jwt, request)
    
    if (!authUser) {
      set.status = 401
      return { success: false, message: 'Unauthorized' }
    }

    // Verify userId matches token
    if (params.userId !== authUser.userId) {
      set.status = 403
      return { success: false, message: 'Forbidden' }
    }

    try {
      // Convert string userId to ObjectId for query
      const userIdObjectId = new mongoose.Types.ObjectId(authUser.userId)
      
      const userResults = await TestResult.find({ userId: userIdObjectId })
        .sort({ completedAt: -1 })
        .lean()

      // Convert Map to object for each result
      const formattedResults = userResults.map(result => ({
        id: result._id,
        userId: result.userId,
        answers: result.answers instanceof Map 
          ? Object.fromEntries(result.answers) 
          : result.answers,
        results: result.results,
        completedAt: result.completedAt
      }))

      return { success: true, results: formattedResults }
    } catch (error) {
      console.error('Get test results error:', error)
      set.status = 500
      return { success: false, message: 'Internal server error' }
    }
  })

