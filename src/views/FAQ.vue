<template>
  <v-container class="py-8">
    <v-row justify="center">
      <v-col cols="12" md="10">
        <!-- Header -->
        <div class="text-center mb-8">
          <v-icon size="64" color="primary" class="mb-4">mdi-frequently-asked-questions</v-icon>
          <h1 class="text-h3 font-weight-bold mb-4">Frequently Asked Questions</h1>
          <p class="text-h6 text-grey">Find answers to common questions about our Career Advisory Platform</p>
        </div>

        <!-- Search Bar -->
        <v-text-field
          v-model="searchQuery"
          label="Search FAQs..."
          prepend-inner-icon="mdi-magnify"
          variant="outlined"
          class="mb-6"
          clearable
          density="comfortable"
          hide-details
        ></v-text-field>

        <!-- Category Chips -->
        <div class="d-flex flex-wrap gap-2 mb-6">
          <v-chip
            v-for="category in categories"
            :key="category.id"
            :color="selectedCategory === category.id ? 'primary' : 'default'"
            :variant="selectedCategory === category.id ? 'flat' : 'outlined'"
            @click="selectedCategory = selectedCategory === category.id ? null : category.id"
            class="mr-2 mb-2"
          >
            <v-icon start size="small">{{ category.icon }}</v-icon>
            {{ category.name }}
            <v-badge
              :content="getCategoryCount(category.id)"
              inline
              color="grey"
              class="ml-2"
            ></v-badge>
          </v-chip>
        </div>

        <!-- No Results Message -->
        <v-alert
          v-if="filteredFaqs.length === 0"
          type="info"
          variant="tonal"
          class="mb-6"
        >
          <div class="d-flex align-center">
            <div>
              <strong>No matching questions found.</strong>
              <p class="mb-0 mt-1">Try different keywords or use our Career Assistant chatbot for personalized help.</p>
            </div>
          </div>
        </v-alert>

        <!-- FAQ Sections -->
        <div v-for="category in categoriesWithFaqs" :key="category.id" class="mb-6">
          <div class="d-flex align-center mb-3">
            <v-icon :color="category.color" class="mr-2">{{ category.icon }}</v-icon>
            <h2 class="text-h6 font-weight-bold mb-0">{{ category.name }}</h2>
          </div>
          
          <v-expansion-panels variant="accordion" class="faq-panels">
            <v-expansion-panel
              v-for="faq in category.faqs"
              :key="faq.id"
              elevation="1"
              class="mb-2"
            >
              <v-expansion-panel-title>
                <div class="d-flex align-center">
                  <v-icon size="small" color="primary" class="mr-3">mdi-help-circle-outline</v-icon>
                  <span class="font-weight-medium">{{ faq.question }}</span>
                </div>
              </v-expansion-panel-title>
              <v-expansion-panel-text>
                <div class="faq-answer" v-html="faq.answer"></div>
              </v-expansion-panel-text>
            </v-expansion-panel>
          </v-expansion-panels>
        </div>

        <!-- Quick Links Section -->
        <v-card class="mb-6" elevation="2">
          <v-card-title class="bg-primary text-white">
            <v-icon class="mr-2">mdi-lightning-bolt</v-icon>
            Quick Actions
          </v-card-title>
          <v-card-text class="pa-4">
            <v-row>
              <v-col cols="12" sm="6" md="3">
                <v-btn
                  block
                  color="primary"
                  variant="tonal"
                  :to="{ name: 'CareerTest' }"
                  prepend-icon="mdi-clipboard-list"
                  class="py-6"
                >
                  Take Career Test
                </v-btn>
              </v-col>
              <v-col cols="12" sm="6" md="3">
                <v-btn
                  block
                  color="success"
                  variant="tonal"
                  :to="{ name: 'Results' }"
                  prepend-icon="mdi-chart-bar"
                  class="py-6"
                >
                  View Results
                </v-btn>
              </v-col>
              <v-col cols="12" sm="6" md="3">
                <v-btn
                  block
                  color="info"
                  variant="tonal"
                  :to="{ name: 'Profile' }"
                  prepend-icon="mdi-account"
                  class="py-6"
                >
                  My Profile
                </v-btn>
              </v-col>
              <v-col cols="12" sm="6" md="3">
                <v-btn
                  block
                  color="warning"
                  variant="tonal"
                  :to="{ name: 'Register' }"
                  prepend-icon="mdi-account-plus"
                  class="py-6"
                >
                  Create Account
                </v-btn>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>

        <!-- Still Need Help Section -->
        <v-card elevation="3" class="help-card">
          <v-row no-gutters>
            <v-col cols="12" md="8" class="pa-6">
              <h2 class="text-h5 font-weight-bold mb-3">Still have questions?</h2>
              <p class="text-body-1 mb-4">
                Can't find what you're looking for? Our AI Career Assistant is available 24/7 to help you with personalized guidance on careers, skills, interview preparation, and more.
              </p>
              <div class="d-flex flex-wrap gap-3">
                <v-btn
                  color="primary"
                  size="large"
                  prepend-icon="mdi-robot"
                  @click="openChatbot"
                >
                  Chat with Career Assistant
                </v-btn>
                <v-btn
                  variant="outlined"
                  size="large"
                  prepend-icon="mdi-email"
                  href="mailto:support@advisorysystem.com"
                >
                  Email Support
                </v-btn>
              </div>
            </v-col>
            <v-col cols="12" md="4" class="d-none d-md-flex align-center justify-center bg-primary">
              <v-icon size="120" color="white" class="opacity-80">mdi-face-agent</v-icon>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'FAQ',
  data() {
    return {
      searchQuery: '',
      selectedCategory: null,
      categories: [
        { id: 'getting-started', name: 'Getting Started', icon: 'mdi-rocket-launch', color: 'primary' },
        { id: 'career-test', name: 'Career Test', icon: 'mdi-clipboard-list', color: 'orange' },
        { id: 'results', name: 'Understanding Results', icon: 'mdi-chart-bar', color: 'success' },
        { id: 'account', name: 'Account & Profile', icon: 'mdi-account-cog', color: 'info' },
        { id: 'career-guidance', name: 'Career Guidance', icon: 'mdi-briefcase', color: 'purple' }
      ],
      faqs: [
        // Getting Started
        {
          id: 1,
          category: 'getting-started',
          question: 'What is the Career Advisory System?',
          answer: `
            <p>The Career Advisory System is a <strong>free career counseling platform</strong> designed to help students and professionals discover their ideal career paths in the IT and technology sector.</p>
            <p><strong>Key Features:</strong></p>
            <ul>
              <li>Scientific career assessment quiz based on your interests and aptitudes</li>
              <li>Personalized career recommendations across 4 major IT fields</li>
              <li>AI-powered Career Assistant for guidance and advice</li>
              <li>Detailed results with specific job role suggestions</li>
              <li>Development tips and learning recommendations</li>
            </ul>
            <p>Our goal is to help you make informed decisions about your career path based on your unique strengths and interests.</p>
          `
        },
        {
          id: 2,
          category: 'getting-started',
          question: 'How do I get started?',
          answer: `
            <p>Getting started is easy and takes just a few minutes:</p>
            <ol>
              <li><strong>Create an Account:</strong> Click "Register" and fill in your details (optional but recommended to save your results)</li>
              <li><strong>Take the Career Test:</strong> Navigate to "Career Test" from the menu</li>
              <li><strong>Answer Honestly:</strong> Complete all questions based on your genuine preferences</li>
              <li><strong>View Your Results:</strong> Get instant personalized career recommendations</li>
              <li><strong>Explore Further:</strong> Use our AI Career Assistant for detailed guidance</li>
            </ol>
            <p><em>Tip: You can take the test without an account, but creating one lets you save and track your results over time.</em></p>
          `
        },
        {
          id: 3,
          category: 'getting-started',
          question: 'Is the platform free to use?',
          answer: `
            <p><strong>Yes! The Career Advisory System is completely free.</strong></p>
            <p>All features are available at no cost, including:</p>
            <ul>
              <li>✅ Full career assessment test</li>
              <li>✅ Detailed results and recommendations</li>
              <li>✅ AI Career Assistant chatbot</li>
              <li>✅ Profile management</li>
              <li>✅ Results history (with account)</li>
              <li>✅ Downloadable results report</li>
            </ul>
            <p>We believe career guidance should be accessible to everyone.</p>
          `
        },
        {
          id: 4,
          category: 'getting-started',
          question: 'Who is this platform for?',
          answer: `
            <p>Our platform is designed for anyone exploring careers in technology and IT:</p>
            <ul>
              <li><strong>High School Students:</strong> Exploring future career options and college majors</li>
              <li><strong>University Students:</strong> Confirming their field of study or considering specializations</li>
              <li><strong>Recent Graduates:</strong> Preparing to enter the job market</li>
              <li><strong>Career Changers:</strong> Professionals looking to transition into tech</li>
              <li><strong>Working Professionals:</strong> Seeking career advancement or new directions</li>
            </ul>
            <p>Whether you're just starting out or looking to make a change, our assessment can help clarify your path.</p>
          `
        },
        
        // Career Test
        {
          id: 5,
          category: 'career-test',
          question: 'How long does the career test take?',
          answer: `
            <p>The career assessment typically takes <strong>10-15 minutes</strong> to complete.</p>
            <p><strong>Test Details:</strong></p>
            <ul>
              <li>Multiple questions across different categories</li>
              <li>5-point scale responses (Strongly Disagree to Strongly Agree)</li>
              <li>Progress bar shows your completion status</li>
              <li>Your answers are automatically saved as you progress</li>
            </ul>
            <p><strong>Tips for Best Results:</strong></p>
            <ul>
              <li>Find a quiet place without distractions</li>
              <li>Answer based on your genuine feelings, not what you think is "correct"</li>
              <li>Don't overthink - your first instinct is usually best</li>
              <li>Be honest with yourself about your preferences</li>
            </ul>
          `
        },
        {
          id: 6,
          category: 'career-test',
          question: 'What types of questions are on the test?',
          answer: `
            <p>The test evaluates your preferences across four key career dimensions:</p>
            <ol>
              <li><strong>Technical Aptitude:</strong> Interest in programming, problem-solving, and building systems</li>
              <li><strong>Business Orientation:</strong> Interest in management, analysis, and organizational processes</li>
              <li><strong>Creative Expression:</strong> Interest in design, user experience, and visual communication</li>
              <li><strong>Interdisciplinary Thinking:</strong> Interest in innovation and combining technology with other fields</li>
            </ol>
            <p>Questions are divided into parts, each focusing on different aspects. You'll rate statements like:</p>
            <ul>
              <li>"I enjoy solving complex logical problems"</li>
              <li>"I like leading and organizing team projects"</li>
              <li>"I appreciate beautiful and user-friendly designs"</li>
            </ul>
          `
        },
        {
          id: 7,
          category: 'career-test',
          question: 'Can I retake the test?',
          answer: `
            <p><strong>Yes, you can retake the test anytime!</strong></p>
            <p>Reasons you might want to retake:</p>
            <ul>
              <li>Your interests or circumstances have changed</li>
              <li>You've gained new skills or experiences</li>
              <li>You want to explore different career options</li>
              <li>You rushed through the first time and want more accurate results</li>
            </ul>
            <p><strong>How to Retake:</strong></p>
            <ol>
              <li>Go to the Career Test page</li>
              <li>Your previous answers will be cleared when you start fresh</li>
              <li>Complete the test again with your current mindset</li>
              <li>View your new results</li>
            </ol>
            <p><em>Note: If you have an account, both old and new results are saved for comparison.</em></p>
          `
        },
        {
          id: 8,
          category: 'career-test',
          question: 'Do I need to create an account to take the test?',
          answer: `
            <p><strong>No, an account is not required</strong> to take the career test.</p>
            <p><strong>Without an Account:</strong></p>
            <ul>
              <li>✅ Take the full career test</li>
              <li>✅ View your results immediately</li>
              <li>✅ Download results as a text file</li>
              <li>❌ Results won't be saved after you close the browser</li>
            </ul>
            <p><strong>With an Account:</strong></p>
            <ul>
              <li>✅ All of the above, plus:</li>
              <li>✅ Results saved permanently to your profile</li>
              <li>✅ Track your career exploration over time</li>
              <li>✅ Access results from any device</li>
              <li>✅ Personalized chatbot assistance</li>
            </ul>
            <p>We recommend creating an account if you want to save your results for future reference.</p>
          `
        },
        
        // Results
        {
          id: 9,
          category: 'results',
          question: 'How are my results calculated?',
          answer: `
            <p>Your results are calculated based on your responses across four career categories:</p>
            <p><strong>The Four Career Fields:</strong></p>
            <ol>
              <li><strong>Technical (Software Engineering & CS):</strong> Software Developer, Data Scientist, ML Engineer, Cybersecurity Specialist</li>
              <li><strong>Business (IT Management):</strong> IT Project Manager, Business Analyst, IT Consultant, Product Manager</li>
              <li><strong>Creative (Digital Design & Media):</strong> UI/UX Designer, Front-end Developer, Digital Content Creator</li>
              <li><strong>Interdisciplinary (Emerging Tech):</strong> Tech Entrepreneur, Innovation Consultant, EdTech Developer</li>
            </ol>
            <p><strong>Scoring:</strong></p>
            <ul>
              <li>Each answer contributes to one or more category scores</li>
              <li>Scores range from negative (low fit) to positive (high fit)</li>
              <li>Categories are ranked by your total score</li>
              <li>Your top category represents your strongest career match</li>
            </ul>
          `
        },
        {
          id: 10,
          category: 'results',
          question: 'What do the scores and percentages mean?',
          answer: `
            <p>Your results show a <strong>compatibility score</strong> for each career field:</p>
            <p><strong>Understanding Your Score:</strong></p>
            <ul>
              <li><strong>Higher scores</strong> = Stronger alignment with that career field</li>
              <li><strong>Percentage</strong> = How well you match compared to the maximum possible score</li>
              <li><strong>Ranking</strong> = Fields are ordered from best to least fit</li>
            </ul>
            <p><strong>Score Interpretation:</strong></p>
            <ul>
              <li><strong>75-100%:</strong> Excellent fit - strongly aligned with your interests</li>
              <li><strong>50-74%:</strong> Good fit - worth exploring further</li>
              <li><strong>25-49%:</strong> Moderate fit - some aspects may appeal to you</li>
              <li><strong>0-24%:</strong> Lower fit - may not match your preferences</li>
            </ul>
            <p><em>Remember: These are suggestions based on your responses, not absolute predictions. Explore all options that interest you!</em></p>
          `
        },
        {
          id: 11,
          category: 'results',
          question: 'Can I download or share my results?',
          answer: `
            <p><strong>Yes!</strong> You can download your results for future reference.</p>
            <p><strong>Download Options:</strong></p>
            <ul>
              <li>Click the "Download Results" button on the Results page</li>
              <li>Results are saved as a text file with all your career recommendations</li>
              <li>Includes scores, career suggestions, and development tips</li>
            </ul>
            <p><strong>What's Included:</strong></p>
            <ul>
              <li>Your top career field recommendations (ranked)</li>
              <li>Specific job roles for each field</li>
              <li>Compatibility scores</li>
              <li>Personalized development suggestions</li>
              <li>Date of assessment</li>
            </ul>
            <p>You can share this file with career counselors, mentors, or keep it for your own planning.</p>
          `
        },
        {
          id: 12,
          category: 'results',
          question: 'What should I do after seeing my results?',
          answer: `
            <p>Your results are just the beginning! Here's what to do next:</p>
            <p><strong>Immediate Next Steps:</strong></p>
            <ol>
              <li><strong>Review All Categories:</strong> Don't just focus on #1 - explore your top 2-3 matches</li>
              <li><strong>Research Job Roles:</strong> Look up the specific careers mentioned in your results</li>
              <li><strong>Chat with Our Assistant:</strong> Ask our AI chatbot for detailed guidance on skills, interview prep, and more</li>
            </ol>
            <p><strong>Planning Your Path:</strong></p>
            <ul>
              <li>Identify skills you need to develop</li>
              <li>Look for online courses or certifications</li>
              <li>Build projects to gain practical experience</li>
              <li>Connect with professionals in your target field</li>
              <li>Update your resume to highlight relevant skills</li>
            </ul>
            <p><strong>Use the Career Assistant</strong> (chat icon at bottom right) for personalized advice on any of these steps!</p>
          `
        },
        
        // Account & Profile
        {
          id: 13,
          category: 'account',
          question: 'How do I create an account?',
          answer: `
            <p>Creating an account is quick and easy:</p>
            <ol>
              <li>Click the <strong>"Register"</strong> button in the top navigation</li>
              <li>Enter your username and password</li>
              <li>Optionally add your department/field of study</li>
              <li>Click "Register" to create your account</li>
              <li>You'll be automatically logged in</li>
            </ol>
            <p><strong>Account Benefits:</strong></p>
            <ul>
              <li>Save your test results permanently</li>
              <li>Track your career exploration journey</li>
              <li>Access your profile from any device</li>
              <li>Get personalized chatbot assistance</li>
            </ul>
          `
        },
        {
          id: 14,
          category: 'account',
          question: 'How do I update my profile information?',
          answer: `
            <p>To update your profile:</p>
            <ol>
              <li>Log in to your account</li>
              <li>Click on your username in the top navigation</li>
              <li>Select <strong>"Profile"</strong> from the dropdown menu</li>
              <li>Update your information (name, email, education details, etc.)</li>
              <li>Click <strong>"Save Changes"</strong></li>
            </ol>
            <p><strong>Profile Information You Can Add:</strong></p>
            <ul>
              <li>Personal details (name, email, phone)</li>
              <li>Identity and gender</li>
              <li>Date of birth</li>
              <li>Education information (school, enrollment year, level)</li>
              <li>Student ID and department</li>
            </ul>
          `
        },
        {
          id: 15,
          category: 'account',
          question: 'I forgot my password. What should I do?',
          answer: `
            <p>If you've forgotten your password, here's what to do:</p>
            <p><strong>Current Options:</strong></p>
            <ul>
              <li>Try common passwords you might have used</li>
              <li>Check if your browser saved the password (Settings → Passwords)</li>
              <li>Create a new account with a different username</li>
            </ul>
            <p><strong>Note:</strong> We're working on adding a password reset feature. In the meantime, if you need assistance, please contact support.</p>
            <p><em>Tip: Use a password manager to securely store your passwords for the future!</em></p>
          `
        },
        {
          id: 16,
          category: 'account',
          question: 'Is my data secure and private?',
          answer: `
            <p><strong>Yes, we take your privacy seriously.</strong></p>
            <p><strong>Data Protection:</strong></p>
            <ul>
              <li>Your test results are only visible to you</li>
              <li>We don't sell or share your personal information</li>
              <li>Passwords are securely encrypted</li>
              <li>You can delete your data by clearing your browser storage</li>
            </ul>
            <p><strong>What We Store:</strong></p>
            <ul>
              <li>Account information (username, profile details)</li>
              <li>Test answers and results</li>
              <li>Chat history with the Career Assistant (stored locally)</li>
            </ul>
            <p><strong>What We Don't Store:</strong></p>
            <ul>
              <li>Payment information (the platform is free)</li>
              <li>Sensitive personal identifiers</li>
              <li>Data shared with third parties</li>
            </ul>
          `
        },
        
        // Career Guidance
        {
          id: 17,
          category: 'career-guidance',
          question: 'What is the AI Career Assistant and how do I use it?',
          answer: `
            <p>The <strong>AI Career Assistant</strong> is your personal career guide available 24/7.</p>
            <p><strong>How to Access:</strong></p>
            <ul>
              <li>Click the <strong>chat icon</strong> (💬) in the bottom-right corner of any page</li>
              <li>Type your question and press Enter or click Send</li>
            </ul>
            <p><strong>What It Can Help With:</strong></p>
            <ul>
              <li>📊 <strong>Explain your test results</strong> - understand what your scores mean</li>
              <li>💼 <strong>Career advice</strong> - learn about different job roles and paths</li>
              <li>📚 <strong>Skill recommendations</strong> - what to learn for your target career</li>
              <li>📝 <strong>Resume tips</strong> - how to write an effective CV</li>
              <li>🎯 <strong>Interview preparation</strong> - common questions and how to answer</li>
              <li>🔍 <strong>Job search strategies</strong> - where and how to find opportunities</li>
            </ul>
            <p><em>The assistant knows your quiz results (if completed) and can give personalized advice!</em></p>
          `
        },
        {
          id: 18,
          category: 'career-guidance',
          question: 'What career fields does the platform cover?',
          answer: `
            <p>Our platform focuses on <strong>IT and Technology careers</strong> across four main areas:</p>
            <p><strong>1. Software Engineering & Computer Science</strong></p>
            <ul>
              <li>Software Developer</li>
              <li>Data Scientist</li>
              <li>Machine Learning Engineer</li>
              <li>Systems Architect</li>
              <li>Cybersecurity Specialist</li>
            </ul>
            <p><strong>2. Business Information Systems & IT Management</strong></p>
            <ul>
              <li>IT Project Manager</li>
              <li>Business Analyst</li>
              <li>IT Consultant</li>
              <li>Product Manager</li>
              <li>Data Analyst</li>
            </ul>
            <p><strong>3. Digital Design & Media Technology</strong></p>
            <ul>
              <li>UI/UX Designer</li>
              <li>Front-end Developer</li>
              <li>Digital Content Creator</li>
              <li>Interactive Media Designer</li>
              <li>Web Designer</li>
            </ul>
            <p><strong>4. Interdisciplinary IT & Emerging Technologies</strong></p>
            <ul>
              <li>Tech Entrepreneur</li>
              <li>Innovation Consultant</li>
              <li>Digital Transformation Specialist</li>
              <li>EdTech Developer</li>
              <li>HealthTech Specialist</li>
            </ul>
          `
        },
        {
          id: 19,
          category: 'career-guidance',
          question: 'How can I learn more about specific careers?',
          answer: `
            <p>There are several ways to explore careers in depth:</p>
            <p><strong>On Our Platform:</strong></p>
            <ul>
              <li><strong>AI Career Assistant:</strong> Ask specific questions like "What does a Data Scientist do?" or "What skills do I need for UX design?"</li>
              <li><strong>Your Results Page:</strong> Click on each career field to see detailed descriptions and job roles</li>
            </ul>
            <p><strong>External Resources:</strong></p>
            <ul>
              <li><strong>LinkedIn:</strong> Search for job titles and see real professionals' profiles</li>
              <li><strong>Glassdoor:</strong> Read about salaries, interviews, and company reviews</li>
              <li><strong>YouTube:</strong> Watch "day in the life" videos from people in different roles</li>
              <li><strong>Reddit:</strong> Communities like r/cscareerquestions offer real insights</li>
            </ul>
            <p><strong>Learning Platforms:</strong></p>
            <ul>
              <li>Coursera, Udemy, freeCodeCamp - for skill-specific courses</li>
              <li>LinkedIn Learning - professional development</li>
              <li>Google Career Certificates - industry-recognized credentials</li>
            </ul>
          `
        },
        {
          id: 20,
          category: 'career-guidance',
          question: 'Can the platform help me prepare for job interviews?',
          answer: `
            <p><strong>Yes!</strong> Our AI Career Assistant can help you prepare for interviews.</p>
            <p><strong>Ask the Assistant About:</strong></p>
            <ul>
              <li>Common interview questions for your target role</li>
              <li>Technical interview preparation tips</li>
              <li>Behavioral interview techniques (STAR method)</li>
              <li>Questions to ask your interviewer</li>
              <li>Salary negotiation basics</li>
              <li>How to present your skills and experience</li>
            </ul>
            <p><strong>Example Questions to Ask:</strong></p>
            <ul>
              <li>"What are common interview questions for software developers?"</li>
              <li>"How do I prepare for a technical interview?"</li>
              <li>"What is the STAR method for behavioral interviews?"</li>
              <li>"How should I negotiate salary for my first job?"</li>
            </ul>
            <p>Just open the chat and start asking! The assistant will provide tailored advice based on your career interests.</p>
          `
        }
      ]
    }
  },
  computed: {
    filteredFaqs() {
      let result = this.faqs
      
      // Filter by search query
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        result = result.filter(faq => 
          faq.question.toLowerCase().includes(query) ||
          faq.answer.toLowerCase().includes(query)
        )
      }
      
      // Filter by category
      if (this.selectedCategory) {
        result = result.filter(faq => faq.category === this.selectedCategory)
      }
      
      return result
    },
    categoriesWithFaqs() {
      return this.categories
        .map(category => ({
          ...category,
          faqs: this.filteredFaqs.filter(faq => faq.category === category.id)
        }))
        .filter(category => category.faqs.length > 0)
    }
  },
  methods: {
    getCategoryCount(categoryId) {
      return this.faqs.filter(faq => faq.category === categoryId).length
    },
    openChatbot() {
      // Emit event to open chatbot or find the chatbot component
      const chatbotBtn = document.querySelector('.chatbot-toggle-btn')
      if (chatbotBtn) {
        chatbotBtn.click()
      }
    }
  }
}
</script>

<style scoped>
.faq-panels .v-expansion-panel {
  border-radius: 8px !important;
  margin-bottom: 8px;
}

.faq-panels .v-expansion-panel-title {
  font-size: 1rem;
}

.faq-answer {
  padding: 8px 0;
  line-height: 1.7;
}

.faq-answer :deep(p) {
  margin-bottom: 12px;
}

.faq-answer :deep(ul),
.faq-answer :deep(ol) {
  margin-bottom: 12px;
  padding-left: 24px;
}

.faq-answer :deep(li) {
  margin-bottom: 6px;
}

.faq-answer :deep(strong) {
  color: #1565C0;
}

.help-card {
  overflow: hidden;
  border-radius: 12px;
}

.gap-2 {
  gap: 8px;
}

.gap-3 {
  gap: 12px;
}
</style>
