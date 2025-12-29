import { readFileSync } from 'fs'
import { fileURLToPath } from 'url'
import { dirname, join } from 'path'
import connectDB from '../src/config/database.js'
import Question from '../src/models/Question.js'

const __filename = fileURLToPath(import.meta.url)
const __dirname = dirname(__filename)

async function seedQuestions() {
  try {
    console.log('🌱 Starting question seeding process...')
    
    // Connect to MongoDB
    await connectDB()
    console.log('✅ Connected to MongoDB')

    // Read questions from JSON file
    const questionsPath = join(__dirname, '../src/question.json')
    const questionsData = JSON.parse(readFileSync(questionsPath, 'utf-8'))
    console.log(`📖 Read ${questionsData.length} questions from file`)

    // Drop the entire collection to clear old indexes
    try {
      await Question.collection.drop()
      console.log('🗑️  Dropped existing questions collection (including indexes)')
    } catch (error) {
      if (error.code === 26) {
        console.log('ℹ️  Collection does not exist yet')
      } else {
        throw error
      }
    }

    // Transform and insert questions
    const questionsToInsert = questionsData.map(q => ({
      questionId: q.id,
      part: parseInt(q.part),
      partTitle: q.partTitle,
      partObjective: q.partObjective,
      question: q.question,
      category: q.category
    }))

    const result = await Question.insertMany(questionsToInsert)
    console.log(`✅ Successfully inserted ${result.length} questions`)

    // Show summary by category
    const summary = await Question.aggregate([
      {
        $group: {
          _id: '$category',
          count: { $sum: 1 }
        }
      },
      {
        $sort: { _id: 1 }
      }
    ])

    console.log('\n📊 Questions by category:')
    summary.forEach(s => {
      console.log(`   ${s._id}: ${s.count}`)
    })

    // Show summary by part
    const partSummary = await Question.aggregate([
      {
        $group: {
          _id: '$part',
          count: { $sum: 1 }
        }
      },
      {
        $sort: { _id: 1 }
      }
    ])

    console.log('\n📊 Questions by part:')
    partSummary.forEach(s => {
      console.log(`   Part ${s._id}: ${s.count}`)
    })

    console.log('\n🎉 Seeding completed successfully!')
    process.exit(0)
  } catch (error) {
    console.error('❌ Error seeding questions:', error)
    process.exit(1)
  }
}

// Run the seed function
seedQuestions()
