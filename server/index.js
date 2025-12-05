import { Elysia } from 'elysia'
import { cors } from '@elysiajs/cors'
import { jwt } from '@elysiajs/jwt'
import { readFile, writeFile } from 'fs/promises'
import { join } from 'path'
import bcrypt from 'bcryptjs'

const DB_PATH = join(import.meta.dir, 'db.json')
const SALT_ROUNDS = 10

const ACCESS_TOKEN_SECRET = process.env.ACCESS_TOKEN_SECRET || 'your-access-token-secret-key-change-in-production'
const REFRESH_TOKEN_SECRET = process.env.REFRESH_TOKEN_SECRET || 'your-refresh-token-secret-key-change-in-production'

// Gemini API Configuration
const GEMINI_API_KEY = process.env.GEMINI_API_KEY
const GEMINI_API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent'

if (!GEMINI_API_KEY) {
  console.warn('⚠️  GEMINI_API_KEY is not set. Chatbot functionality will be disabled.')
}

// System prompt for the AI Career Assistant
const SYSTEM_PROMPT = `You are the Job Assistant for the Job Quiz web application - an AI career counselor specialized in helping users discover and pursue their ideal career paths. You provide practical, actionable job-related guidance.

App Routes (use these exact paths for navigation):
- Home: /
- Career Test: /career-test
- Results: /results
- Profile: /profile
- Login: /login
- Register: /register
- FAQ: /faq
- About: /about

Career Categories in the Quiz:
1. TECHNICAL (Software Engineering & Computer Science): Software Developer, Data Scientist, ML Engineer, Systems Architect, Cybersecurity Specialist
2. BUSINESS (Business Information Systems & IT Management): IT Project Manager, Business Analyst, IT Consultant, Product Manager, Data Analyst
3. CREATIVE (Digital Design & Media Technology): UI/UX Designer, Front-end Developer, Digital Content Creator, Interactive Media Designer, Web Designer
4. INTERDISCIPLINARY (Interdisciplinary IT & Emerging Technologies): Tech Entrepreneur, Innovation Consultant, Digital Transformation Specialist, EdTech Developer, HealthTech Specialist

Persona & tone:
- Friendly, encouraging career coach who genuinely wants to help users succeed
- Concise and practical - focus on actionable advice
- Use bullet points and numbered lists for clarity
- If the user's language indicates Vietnamese (user.lang === "vi"), respond in Vietnamese

CORE CAPABILITIES - Provide helpful guidance on:

1. CAREER EXPLORATION & ADVICE:
   - Explain what different IT/tech careers involve day-to-day
   - Discuss pros/cons of different career paths
   - Help users understand which careers match their quiz results
   - Provide industry insights and job market trends
   - Suggest career paths based on interests and strengths

2. SKILL DEVELOPMENT GUIDANCE:
   - Recommend specific technical skills to learn for each career
   - Suggest free/paid learning resources (Coursera, Udemy, freeCodeCamp, etc.)
   - Recommend certifications (AWS, Google, Microsoft, CompTIA, etc.)
   - Provide learning roadmaps for different career paths
   - Suggest portfolio projects to build

3. JOB SEARCH STRATEGIES:
   - Tips for writing effective resumes/CVs for tech roles
   - LinkedIn profile optimization advice
   - Job board recommendations (LinkedIn, Indeed, Glassdoor, AngelList, etc.)
   - Networking strategies and tips
   - How to find internships and entry-level positions

4. INTERVIEW PREPARATION:
   - Common interview questions for different tech roles
   - Technical interview preparation tips
   - Behavioral interview (STAR method) guidance
   - Salary negotiation basics
   - Questions to ask interviewers

5. CAREER TRANSITION SUPPORT:
   - Advice for switching between tech fields
   - Transferable skills identification
   - Realistic timelines for career changes
   - First steps for career changers

6. QUIZ & RESULTS GUIDANCE:
   - Explain test instructions and question types
   - Help interpret quiz results
   - Suggest next steps based on results
   - Encourage retaking if results seem off

RESPONSE GUIDELINES:
- If user has completed quiz, reference their specific results to personalize advice
- Always provide 2-3 actionable next steps
- Include relevant quick reply options for follow-up questions
- Be encouraging but realistic about career expectations
- For salary questions, give ranges and note they vary by location/experience

LIMITATIONS - Do NOT:
- Make API calls or modify user data
- Provide medical, legal, or financial advice
- Ask for sensitive info (passwords, payment details, ID numbers)
- Guarantee job outcomes or make promises about employment
- Pretend to submit applications or contact employers

Response format (MUST be valid JSON):
{
  "reply": "Your helpful response here (can include line breaks with \\n for formatting)",
  "action": null | { "type": "navigate", "target": "/results" },
  "quickReplies": ["Relevant", "Follow-up", "Options"],
  "metadata": { "confidence": 0.9 }
}

Always respond in valid JSON. The "reply" field contains your main response text.`

/**
 * Builds the context-aware prompt for the AI
 */
function buildChatPrompt(userMessage, context) {
  let prompt = SYSTEM_PROMPT + '\n\n'
  
  // Add context information
  if (context) {
    prompt += 'Current Context:\n'
    
    if (context.user) {
      prompt += `- User: ${context.user.name || 'Guest'} (ID: ${context.user.id || 'N/A'}, Language: ${context.user.lang || 'en'}, Authenticated: ${context.user.auth || false})\n`
    }
    
    if (context.currentPage) {
      prompt += `- Current Page: ${context.currentPage}\n`
    }
    
    if (context.testState) {
      prompt += `- Test State: Test ID ${context.testState.testId}, Question ${context.testState.questionIndex + 1}, Progress: ${(context.testState.progress * 100).toFixed(0)}%\n`
    }
    
    if (context.latestResultSummary) {
      prompt += `- Has Completed Quiz: ${context.latestResultSummary.hasCompletedQuiz ? 'Yes' : 'No'}\n`
      if (context.latestResultSummary.hasCompletedQuiz) {
        prompt += `- Quiz Results Summary:\n`
        prompt += `  * Top Career Match: ${context.latestResultSummary.topCareerField || 'N/A'}\n`
        prompt += `  * Top Score: ${context.latestResultSummary.score}/${context.latestResultSummary.maxScore} (${context.latestResultSummary.percentage}% match)\n`
        prompt += `  * Career Rankings: ${context.latestResultSummary.allRecommendations?.join(' > ') || 'N/A'}\n`
        prompt += `  * All Scores: ${context.latestResultSummary.detailedScores || 'N/A'}\n`
        prompt += `\nUse these results to personalize career advice. Reference specific careers from their top match category.\n`
      }
    }
    
    prompt += '\n'
  }
  
  // Determine language preference
  const userLang = context?.user?.lang || 'en'
  if (userLang === 'vi') {
    prompt += 'User is Vietnamese. Respond in Vietnamese unless they explicitly ask in English.\n\n'
  }
  
  prompt += `User Message: ${userMessage}\n\n`
  prompt += 'Provide your response as a JSON object following the specified format.'
  
  return prompt
}

async function getDB() {
  const data = await readFile(DB_PATH, 'utf-8')
  return JSON.parse(data)
}

async function saveDB(db) {
  await writeFile(DB_PATH, JSON.stringify(db, null, 2))
}

const app = new Elysia()
  .use(cors())
  .use(
    jwt({
      name: 'jwt',
      secret: ACCESS_TOKEN_SECRET
    })
  )
  .use(
    jwt({
      name: 'refreshJwt',
      secret: REFRESH_TOKEN_SECRET
    })
  )
  .post('/register', async ({ body, set, jwt, refreshJwt }) => {
    // Accept extended profile fields. Many are optional; require basic auth fields.
    const {
      username,
      password,
      department,

      // profile fields (optional)
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

    const db = await getDB()
    const existingUser = db.users.find(u => u.username === username)
    if (existingUser) {
      set.status = 400
      return { success: false, message: 'Username already exists' }
    }

    // Hash password before storing
    console.log('Hashing password with bcryptjs...')
    const hashedPassword = await bcrypt.hash(password, SALT_ROUNDS)
    console.log('Password hashed successfully')

    const user = {
      id: Date.now(),
      username,
      password: hashedPassword,
      department,
      profile: {
        identity: identity || null,
        gender: gender || null,
        accountNumber: accountNumber || null,
        name: name || null,
        // dateOfBirth can be an ISO string or an object { year, month, day }
        dateOfBirth: dateOfBirth || null,
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
    }

    db.users.push(user)
    console.log('Saving user with profile:', JSON.stringify(user.profile, null, 2))

    // Generate tokens
    const accessToken = await jwt.sign({
      userId: user.id,
      username: user.username,
      type: 'access'
    })

    const refreshToken = await refreshJwt.sign({
      userId: user.id,
      username: user.username,
      type: 'refresh'
    })

    // Store refresh token
    if (!db.refreshTokens) db.refreshTokens = []
    db.refreshTokens.push({
      userId: user.id,
      token: refreshToken,
      createdAt: new Date().toISOString()
    })
    
    // Save database once after all operations
    await saveDB(db)

    return {
      success: true,
      user: { id: user.id, username: user.username, department: user.department, profile: user.profile },
      accessToken,
      refreshToken
    }
  })
  .post('/login', async ({ body, set, jwt, refreshJwt }) => {
    const { username, password } = body
    
    if (!username || !password) {
      set.status = 400
      return { success: false, message: 'Username and password are required' }
    }

    const db = await getDB()
    const user = db.users.find(u => u.username === username)

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
      userId: user.id,
      username: user.username,
      type: 'access'
    })

    const refreshToken = await refreshJwt.sign({
      userId: user.id,
      username: user.username,
      type: 'refresh'
    })

    // Store refresh token
    if (!db.refreshTokens) db.refreshTokens = []
    db.refreshTokens.push({
      userId: user.id,
      token: refreshToken,
      createdAt: new Date().toISOString()
    })
    
    // Save database once after all operations
    await saveDB(db)

    return {
      success: true,
      user: { id: user.id, username: user.username, department: user.department, profile: user.profile || null },
      accessToken,
      refreshToken
    }
  })
  .post('/refresh', async ({ body, set, jwt, refreshJwt }) => {
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
      const db = await getDB()
      const tokenExists = db.refreshTokens?.some(t => t.token === refreshToken && t.userId === payload.userId)
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
      set.status = 401
      return { success: false, message: 'Invalid or expired refresh token' }
    }
  })
  .post('/logout', async ({ body }) => {
    const { refreshToken } = body
    if (refreshToken) {
      const db = await getDB()
      if (db.refreshTokens) {
        db.refreshTokens = db.refreshTokens.filter(t => t.token !== refreshToken)
        await saveDB(db)
      }
    }
    return { success: true, message: 'Logged out successfully' }
  })
  .post('/test-results', async ({ body, set, jwt, request }) => {
    // Verify JWT token
    const authHeader = request.headers.get('authorization')
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      set.status = 401
      return { success: false, message: 'Unauthorized' }
    }

    const token = authHeader.substring(7)
    let payload
    try {
      payload = await jwt.verify(token)
      if (!payload || payload.type !== 'access') {
        set.status = 401
        return { success: false, message: 'Invalid token' }
      }
    } catch (error) {
      set.status = 401
      return { success: false, message: 'Invalid or expired token' }
    }

    const { userId, answers, results } = body
    if (!userId || !answers || !results) {
      set.status = 400
      return { success: false, message: 'Missing fields' }
    }

    // Verify userId matches token (convert to number for comparison)
    if (Number(userId) !== payload.userId) {
      set.status = 403
      return { success: false, message: 'Forbidden' }
    }

    const db = await getDB()
    if (!db.testResults) {
      db.testResults = []
    }

    const testResult = {
      id: Date.now(),
      userId,
      answers,
      results,
      completedAt: new Date().toISOString()
    }

    db.testResults.push(testResult)
    await saveDB(db)

    return { success: true, testResult }
  })
  .get('/test-results/:userId', async ({ params, set, jwt, request }) => {
    // Verify JWT token
    const authHeader = request.headers.get('authorization')
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      set.status = 401
      return { success: false, message: 'Unauthorized' }
    }

    const token = authHeader.substring(7)
    let payload
    try {
      payload = await jwt.verify(token)
      if (!payload || payload.type !== 'access') {
        set.status = 401
        return { success: false, message: 'Invalid token' }
      }
    } catch (error) {
      set.status = 401
      return { success: false, message: 'Invalid or expired token' }
    }

    // Verify userId matches token
    if (parseInt(params.userId) !== payload.userId) {
      set.status = 403
      return { success: false, message: 'Forbidden' }
    }

    const db = await getDB()
    if (!db.testResults) {
      return { success: true, results: [] }
    }

    const userResults = db.testResults.filter(r => r.userId === parseInt(params.userId))
    return { success: true, results: userResults }
  })
  .get('/questions', async () => {
    const db = await getDB()
    return { success: true, questions: db.questions || [] }
  })
  .put('/users/:userId/profile', async ({ params, body, set, jwt, request }) => {
    // Verify JWT token
    const authHeader = request.headers.get('authorization')
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      set.status = 401
      return { success: false, message: 'Unauthorized' }
    }

    const token = authHeader.substring(7)
    let payload
    try {
      payload = await jwt.verify(token)
      if (!payload || payload.type !== 'access') {
        set.status = 401
        return { success: false, message: 'Invalid token' }
      }
    } catch (error) {
      set.status = 401
      return { success: false, message: 'Invalid or expired token' }
    }

    // Verify userId matches token
    if (parseInt(params.userId) !== payload.userId) {
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

    const db = await getDB()
    const user = db.users.find(u => u.id === parseInt(params.userId))
    
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
      dateOfBirth: dateOfBirth || null,
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

    await saveDB(db)

    return { 
      success: true, 
      message: 'Profile updated successfully',
      user: { 
        id: user.id, 
        username: user.username, 
        department: user.department, 
        profile: user.profile 
      }
    }
  })
  // Chatbot endpoint
  .post('/chat', async ({ body, set }) => {
    const { message, context } = body
    
    if (!message) {
      set.status = 400
      return { success: false, message: 'Message is required' }
    }
    
    if (!GEMINI_API_KEY) {
      const userLang = context?.user?.lang || 'en'
      const errorMessage = userLang === 'vi' 
        ? 'Chatbot chưa được cấu hình. Vui lòng liên hệ quản trị viên.'
        : 'Chatbot is not configured. Please contact the administrator.'
      
      return {
        success: true,
        response: {
          reply: errorMessage,
          action: null,
          quickReplies: [],
          metadata: { confidence: 0, error: 'API key not configured' }
        }
      }
    }
    
    try {
      const prompt = buildChatPrompt(message, context)
      
      const response = await fetch(`${GEMINI_API_URL}?key=${GEMINI_API_KEY}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          contents: [{
            parts: [{
              text: prompt
            }]
          }]
        })
      })
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(`API error: ${response.status} - ${errorData.error?.message || response.statusText}`)
      }
      
      const data = await response.json()
      
      // Extract the generated text
      const generatedText = data.candidates?.[0]?.content?.parts?.[0]?.text || ''
      
      if (!generatedText) {
        throw new Error('No response generated from API')
      }
      
      // Try to parse JSON from the response
      let jsonText = generatedText.trim()
      
      // Remove markdown code blocks if present
      if (jsonText.startsWith('```json')) {
        jsonText = jsonText.replace(/^```json\s*/, '').replace(/\s*```$/, '')
      } else if (jsonText.startsWith('```')) {
        jsonText = jsonText.replace(/^```\s*/, '').replace(/\s*```$/, '')
      }
      
      try {
        const parsedResponse = JSON.parse(jsonText)
        
        // Validate response structure
        if (!parsedResponse.reply) {
          return {
            success: true,
            response: {
              reply: generatedText,
              action: null,
              quickReplies: [],
              metadata: { confidence: 0.7 }
            }
          }
        }
        
        return { success: true, response: parsedResponse }
      } catch (parseError) {
        // If JSON parsing fails, return the text as reply
        console.warn('Failed to parse JSON response, using raw text:', parseError.message)
        return {
          success: true,
          response: {
            reply: generatedText,
            action: null,
            quickReplies: [],
            metadata: { confidence: 0.7 }
          }
        }
      }
    } catch (error) {
      console.error('Chatbot API error:', error.message)
      
      const userLang = context?.user?.lang || 'en'
      const errorMessage = userLang === 'vi' 
        ? 'Xin lỗi, đã xảy ra lỗi khi xử lý yêu cầu của bạn. Vui lòng thử lại sau.'
        : 'Sorry, an error occurred while processing your request. Please try again later.'
      
      return {
        success: true,
        response: {
          reply: errorMessage,
          action: null,
          quickReplies: [],
          metadata: { confidence: 0, error: error.message }
        }
      }
    }
  })
  .listen(3000)

console.log(`🐹 Elysia is running at ${app.server?.hostname}:${app.server?.port}`)
