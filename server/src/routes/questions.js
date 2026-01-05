import { Elysia } from 'elysia'
import { Question } from '../models/index.js'

export const questionRoutes = new Elysia()
  .get('/questions', async ({ set }) => {
    try {
      const questions = await Question.find()
        .sort({ part: 1, questionId: 1 })
        .lean()

      // Transform to match expected format
      const formattedQuestions = questions.map(q => ({
        id: q.questionId,
        part: q.part,
        partTitle: q.partTitle,
        partObjective: q.partObjective,
        question: q.question,
        category: q.category
      }))

      return { success: true, questions: formattedQuestions }
    } catch (error) {
      console.error('Get questions error:', error)
      set.status = 500
      return { success: false, message: 'Internal server error' }
    }
  })

