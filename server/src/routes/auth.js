import { Elysia } from 'elysia'
import bcrypt from 'bcryptjs'
import { User, RefreshToken } from '../models/index.js'

const SALT_ROUNDS = 10

export const authRoutes = (jwt, refreshJwt) => new Elysia()
  .post('/register', async ({ body, set }) => {
    const {
      username,
      password,
      department,
      // Profile fields (optional)
      identity,
      gender,
      accountNumber,
      name,
      dateOfBirth,
      email,
      mobilePhone,
      enrollmentYear,
      enrollmentLevel,
      schoolCity,
      schoolName,
      durationOfStudy,
      departmentInstitute,
      yearClass,
      studentId,
      agreedToTerms
    } = body

    // Server-side validation
    if (!username || !password || !department) {
      set.status = 400
      return { success: false, message: 'Missing required fields: username, password and department' }
    }

    // Validate username length and format
    if (typeof username !== 'string' || username.length < 3 || username.length > 50) {
      set.status = 400
      return { success: false, message: 'Username must be between 3 and 50 characters' }
    }

    // Validate password strength
    if (typeof password !== 'string' || password.length < 6) {
      set.status = 400
      return { success: false, message: 'Password must be at least 6 characters long' }
    }

    // Validate email format if provided
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (email && !emailRegex.test(email)) {
      set.status = 400
      return { success: false, message: 'Invalid email format' }
    }

    // Validate identity field
    const validIdentities = ['student', 'Unemployed', 'employed']
    if (identity && !validIdentities.includes(identity)) {
      set.status = 400
      return { success: false, message: 'Invalid identity value' }
    }

    // Validate gender field
    const validGenders = ['female', 'male']
    if (gender && !validGenders.includes(gender)) {
      set.status = 400
      return { success: false, message: 'Invalid gender value' }
    }

    // Validate dateOfBirth structure if provided
    if (dateOfBirth && typeof dateOfBirth === 'object') {
      const { year, month, day } = dateOfBirth
      if (year && (year < 1900 || year > new Date().getFullYear())) {
        set.status = 400
        return { success: false, message: 'Invalid birth year' }
      }
      if (month && (month < 1 || month > 12)) {
        set.status = 400
        return { success: false, message: 'Invalid birth month' }
      }
      if (day && (day < 1 || day > 31)) {
        set.status = 400
        return { success: false, message: 'Invalid birth day' }
      }
    }

    try {
      // Check if user already exists
      const existingUser = await User.findOne({ username })
      if (existingUser) {
        set.status = 400
        return { success: false, message: 'Username already exists' }
      }

      // Hash password before storing
      const hashedPassword = await bcrypt.hash(password, SALT_ROUNDS)

      // Create new user
      const user = new User({
        username,
        password: hashedPassword,
        department,
        profile: {
          identity: identity || null,
          gender: gender || null,
          accountNumber: accountNumber || null,
          name: name || null,
          dateOfBirth: dateOfBirth || { year: null, month: null, day: null },
          email: email || null,
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
          agreedToTerms: !!agreedToTerms
        }
      })

      await user.save()

      // Generate tokens
      const accessToken = await jwt.sign({
        userId: user._id.toString(),
        username: user.username,
        type: 'access'
      })

      const refreshToken = await refreshJwt.sign({
        userId: user._id.toString(),
        username: user.username,
        type: 'refresh'
      })

      // Store refresh token
      await RefreshToken.create({
        userId: user._id,
        token: refreshToken
      })

      return {
        success: true,
        user: {
          id: user._id,
          username: user.username,
          department: user.department,
          profile: user.profile
        },
        accessToken,
        refreshToken
      }
    } catch (error) {
      console.error('Registration error:', error)
      set.status = 500
      return { success: false, message: 'Internal server error' }
    }
  })

  .post('/login', async ({ body, set }) => {
    const { username, password } = body

    if (!username || !password) {
      set.status = 400
      return { success: false, message: 'Username and password are required' }
    }

    try {
      const user = await User.findOne({ username })

      if (!user) {
        set.status = 401
        return { success: false, message: 'Invalid credentials' }
      }

      // Verify password hash
      const passwordMatch = await bcrypt.compare(password, user.password)

      if (!passwordMatch) {
        set.status = 401
        return { success: false, message: 'Invalid credentials' }
      }

      // Generate tokens
      const accessToken = await jwt.sign({
        userId: user._id.toString(),
        username: user.username,
        type: 'access'
      })

      const refreshToken = await refreshJwt.sign({
        userId: user._id.toString(),
        username: user.username,
        type: 'refresh'
      })

      // Store refresh token
      await RefreshToken.create({
        userId: user._id,
        token: refreshToken
      })

      return {
        success: true,
        user: {
          id: user._id,
          username: user.username,
          department: user.department,
          profile: user.profile || null
        },
        accessToken,
        refreshToken
      }
    } catch (error) {
      console.error('Login error:', error)
      set.status = 500
      return { success: false, message: 'Internal server error' }
    }
  })

  .post('/refresh', async ({ body, set }) => {
    const { refreshToken } = body

    if (!refreshToken) {
      set.status = 400
      return { success: false, message: 'Refresh token required' }
    }

    try {
      const payload = await refreshJwt.verify(refreshToken)

      if (!payload || payload.type !== 'refresh') {
        set.status = 401
        return { success: false, message: 'Invalid refresh token' }
      }

      // Check if refresh token exists in database
      const tokenExists = await RefreshToken.findOne({
        token: refreshToken,
        userId: payload.userId
      })

      if (!tokenExists) {
        set.status = 401
        return { success: false, message: 'Refresh token not found' }
      }

      // Generate new access token
      const accessToken = await jwt.sign({
        userId: payload.userId,
        username: payload.username,
        type: 'access'
      })

      return { success: true, accessToken }
    } catch (error) {
      console.error('Refresh token error:', error)
      set.status = 401
      return { success: false, message: 'Invalid or expired refresh token' }
    }
  })

  .post('/logout', async ({ body }) => {
    const { refreshToken } = body

    if (refreshToken) {
      try {
        await RefreshToken.deleteOne({ token: refreshToken })
      } catch (error) {
        console.error('Logout error:', error)
      }
    }

    return { success: true, message: 'Logged out successfully' }
  })

