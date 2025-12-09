import { Elysia } from 'elysia'
import mongoose from 'mongoose'
import { TestResult } from '../models/index.js'
import { verifyToken } from '../middleware/auth.js'

export const testRoutes = (jwt) => new Elysia()
  .post('/test-results', async ({ body, set, request }) => {
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

  .get('/test-results/:userId', async ({ params, set, request }) => {
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

