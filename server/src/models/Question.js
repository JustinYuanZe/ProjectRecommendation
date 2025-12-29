import mongoose from 'mongoose'

const questionSchema = new mongoose.Schema({
  questionId: {
    type: String,
    required: true,
    unique: true
  },
  part: {
    type: Number,
    required: true
  },
  partTitle: {
    type: String,
    required: true
  },
  partObjective: {
    type: String,
    required: true
  },
  question: {
    type: String,
    required: true
  },
  category: {
    type: String,
    required: true,
    enum: ['technical', 'business', 'creative', 'interdisciplinary']
  }
}, {
  timestamps: true
})

// Index for faster category-based queries
questionSchema.index({ category: 1 })
questionSchema.index({ part: 1 })

export default mongoose.models.Question || mongoose.model('Question', questionSchema)

