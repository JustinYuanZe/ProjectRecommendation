import { Elysia, t } from 'elysia'
import { GoogleGenerativeAI } from '@google/generative-ai'

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
- If the user's language indicates Traditional Chinese (user.lang === "zh-TW"), respond in Traditional Chinese (繁體中文)
- If the user's language indicates Vietnamese (user.lang === "vi"), respond in Vietnamese
- When mentioning app pages/routes, format them as clickable markdown links using [Page Name](/route-path)
  Example: "Check out the [Results page](/results) for more details"
  Example: "Take the [Career Test](/career-test) to get started"

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
- Be encouraging but realistic about career expectations
- For salary questions, give ranges and note they vary by location/experience
- Do NOT include "Quick Replies:" or suggest follow-up questions in your response - these are handled separately

LIMITATIONS - Do NOT:
- Make API calls or modify user data
- Provide medical, legal, or financial advice
- Ask for sensitive info (passwords, payment details, ID numbers)
- Guarantee job outcomes or make promises about employment
- Pretend to submit applications or contact employers

Always provide helpful, practical career guidance in a friendly and professional tone.`

// Initialize Gemini AI
const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY)

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
  if (userLang === 'zh-TW') {
    prompt += 'User is Taiwanese/Chinese. Respond in Traditional Chinese (繁體中文) unless they explicitly ask in English.\n\n'
  } else if (userLang === 'vi') {
    prompt += 'User is Vietnamese. Respond in Vietnamese unless they explicitly ask in English.\n\n'
  }
  
  prompt += `User Message: ${userMessage}\n\n`
  prompt += 'Provide your helpful response with practical career guidance.'
  
  return prompt
}

/**
 * Generate quick replies based on user message and context
 */
function generateQuickReplies(userMessage, context) {
  const lowerMsg = userMessage.toLowerCase()
  const results = context?.latestResultSummary
  
  // Career/job related queries
  if (lowerMsg.includes('career') || lowerMsg.includes('job') || lowerMsg.includes('result')) {
    if (results?.hasCompletedQuiz) {
      return ['Skills to develop', 'Interview preparation', 'Job search tips']
    }
    return ['Take the career quiz', 'What careers are trending?']
  }
  
  // Interview related
  if (lowerMsg.includes('interview')) {
    return ['Common interview questions', 'Technical interview tips', 'Salary negotiation']
  }
  
  // Resume/CV related
  if (lowerMsg.includes('resume') || lowerMsg.includes('cv')) {
    return ['Resume format tips', 'What to include', 'LinkedIn optimization']
  }
  
  // Skills related
  if (lowerMsg.includes('skill') || lowerMsg.includes('learn')) {
    return ['Free learning resources', 'Recommended certifications', 'Project ideas']
  }
  
  // Default suggestions based on quiz status
  if (results?.hasCompletedQuiz) {
    return ['Explain my results', 'Career advice', 'Next steps']
  }
  return ['Take career quiz', 'How does the quiz work?', 'Career options']
}

export const chatbotRoutes = new Elysia({ prefix: '/api/chatbot' })
  .post('/message', async ({ body, set }) => {
    try {
      const { message, context } = body

      if (!message || typeof message !== 'string' || message.trim().length === 0) {
        set.status = 400
        return { 
          error: 'Message is required and must be a non-empty string' 
        }
      }

      if (!process.env.GEMINI_API_KEY) {
        set.status = 500
        return { 
          error: 'Gemini API key is not configured',
          reply: 'Sorry, the chatbot service is not configured. Please contact support.',
          quickReplies: generateQuickReplies(message, context),
          metadata: { confidence: 0 }
        }
      }

      // Build the context-aware prompt
      const contextPrompt = buildChatPrompt(message, context || {})

      // Initialize the model with system instruction
      const model = genAI.getGenerativeModel({
        model: 'gemini-2.5-flash',
        systemInstruction: SYSTEM_PROMPT,
        generationConfig: {
          temperature: 0.8,
          topP: 0.95,
          topK: 40,
          candidateCount: 1,
        }
      })

      // Generate response
      const result = await model.generateContent(contextPrompt)
      const response = await result.response
      const text = response.text()

      // Generate quick replies
      const quickReplies = generateQuickReplies(message, context)

      return {
        reply: text,
        action: null,
        quickReplies: quickReplies,
        metadata: { 
          confidence: 0.9,
          model: 'gemini-2.5-flash' 
        }
      }

    } catch (error) {
      console.error('Chatbot error:', error)
      set.status = 500

      let errorMessage = 'Sorry, an error occurred while processing your request. Please try again later.'

      return {
        error: error.message,
        reply: errorMessage,
        action: null,
        quickReplies: generateQuickReplies(body?.message || '', body?.context),
        metadata: { confidence: 0, error: error.message }
      }
    }
  }, {
    body: t.Object({
      message: t.String(),
      context: t.Optional(t.Object({
        sessionId: t.Optional(t.String()),
        user: t.Optional(t.Object({
          id: t.Optional(t.Union([t.String(), t.Number()])),
          name: t.Optional(t.String()),
          lang: t.Optional(t.String()),
          auth: t.Optional(t.Boolean())
        })),
        currentPage: t.Optional(t.String()),
        testState: t.Optional(t.Any()),
        latestResultSummary: t.Optional(t.Any())
      }))
    })
  })
