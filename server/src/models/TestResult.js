import mongoose from 'mongoose'

const testResultSchema = new mongoose.Schema({
  userId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true,
    index: true
  },
  answers: {
    type: Map,
    of: Number,
    required: true
  },
  results: {
    topRecommendations: [{
      field: { type: String, required: true },
      score: { type: Number, required: true },
      maxScore: { type: Number, required: true },
      title: { type: String, required: true },
      careers: [{ type: String }],
      description: { type: String }
    }],
    categoryScores: {
      technical: { type: Number, default: 0 },
      business: { type: Number, default: 0 },
      creative: { type: Number, default: 0 },
      interdisciplinary: { type: Number, default: 0 }
    }
  },
  completedAt: {
    type: Date,
    default: Date.now
  }
}, {
  timestamps: true
})

// Index for faster user result lookups
testResultSchema.index({ userId: 1, completedAt: -1 })

export default mongoose.models.TestResult || mongoose.model('TestResult', testResultSchema)

