import mongoose from 'mongoose'

const refreshTokenSchema = new mongoose.Schema({
  userId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true,
    index: true
  },
  token: {
    type: String,
    required: true,
    unique: true
  },
  createdAt: {
    type: Date,
    default: Date.now,
    expires: 60 * 60 * 24 * 7 // Token expires after 7 days (TTL index)
  }
})

// Compound index for faster lookups
refreshTokenSchema.index({ token: 1, userId: 1 })

export default mongoose.models.RefreshToken || mongoose.model('RefreshToken', refreshTokenSchema)

