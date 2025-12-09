import { Elysia } from 'elysia'
import { User } from '../models/index.js'
import { verifyToken } from '../middleware/auth.js'

export const userRoutes = (jwt) => new Elysia()
  .put('/users/:userId/profile', async ({ params, body, set, request }) => {
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

    const {
      identity,
      gender,
      accountNumber,
      name,
      dateOfBirth,
      email,
      backupEmail,
      mobilePhone,
      enrollmentYear,
      enrollmentLevel,
      schoolCity,
      schoolName,
      durationOfStudy,
      departmentInstitute,
      yearClass,
      studentId
    } = body

    // Validate email format if provided
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (email && !emailRegex.test(email)) {
      set.status = 400
      return { success: false, message: 'Invalid email format' }
    }
    if (backupEmail && !emailRegex.test(backupEmail)) {
      set.status = 400
      return { success: false, message: 'Invalid backup email format' }
    }

    try {
      const user = await User.findById(authUser.userId)

      if (!user) {
        set.status = 404
        return { success: false, message: 'User not found' }
      }

      // Update user profile
      user.profile = {
        identity: identity || null,
        gender: gender || null,
        accountNumber: accountNumber || null,
        name: name || null,
        dateOfBirth: dateOfBirth || { year: null, month: null, day: null },
        email: email || null,
        backupEmail: backupEmail || null,
        mobilePhone: mobilePhone || null,
        enrollment: {
          year: enrollmentYear || null,
          level: enrollmentLevel || null
        },
        school: {
          city: schoolCity || null,
          name: schoolName || null
        },
        durationOfStudy: durationOfStudy || null,
        departmentInstitute: departmentInstitute || null,
        yearClass: yearClass || null,
        studentId: studentId || null,
        agreedToTerms: user.profile?.agreedToTerms || false
      }

      await user.save()

      return {
        success: true,
        message: 'Profile updated successfully',
        user: {
          id: user._id,
          username: user.username,
          department: user.department,
          profile: user.profile
        }
      }
    } catch (error) {
      console.error('Update profile error:', error)
      set.status = 500
      return { success: false, message: 'Internal server error' }
    }
  })

