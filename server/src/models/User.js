import mongoose from 'mongoose'

const userSchema = new mongoose.Schema({
  username: {
    type: String,
    required: true,
    unique: true,
    trim: true,
    minlength: 3,
    maxlength: 50
  },
  password: {
    type: String,
    required: true
  },
  department: {
    type: String,
    required: true
  },
  profile: {
    identity: {
      type: String,
      enum: ['student', 'Unemployed', 'employed', null],
      default: null
    },
    gender: {
      type: String,
      enum: ['female', 'male', null],
      default: null
    },
    accountNumber: { type: String, default: null },
    name: { type: String, default: null },
    dateOfBirth: {
      year: { type: Number, default: null },
      month: { type: Number, default: null },
      day: { type: Number, default: null }
    },
    email: { type: String, default: null },
    backupEmail: { type: String, default: null },
    mobilePhone: { type: String, default: null },
    enrollment: {
      year: { type: Number, default: null },
      level: { type: String, default: null }
    },
    school: {
      city: { type: String, default: null },
      name: { type: String, default: null }
    },
    durationOfStudy: { type: String, default: null },
    departmentInstitute: { type: String, default: null },
    yearClass: { type: Number, default: null },
    studentId: { type: String, default: null },
    agreedToTerms: { type: Boolean, default: false }
  }
}, {
  timestamps: true
})

// Note: username already has unique: true which creates an index automatically
// No need for manual index() call

export default mongoose.models.User || mongoose.model('User', userSchema)

