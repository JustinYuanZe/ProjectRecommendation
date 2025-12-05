<template>
  <v-container class="py-8">
    <v-row justify="center">
      <v-col cols="12" md="10">
        <!-- Header -->
        <div class="text-center mb-8">
          <v-icon size="64" color="primary" class="mb-4">mdi-frequently-asked-questions</v-icon>
          <h1 class="text-h3 font-weight-bold mb-4">{{ $t('faq.title') }}</h1>
          <p class="text-h6 text-grey">{{ $t('faq.subtitle') }}</p>
        </div>

        <!-- Search Bar -->
        <v-text-field
          v-model="searchQuery"
          :label="$t('faq.searchPlaceholder')"
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
            v-for="category in translatedCategories"
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
              <strong>{{ $t('faq.noResults') }}</strong>
              <p class="mb-0 mt-1">{{ $t('faq.noResultsHint') }}</p>
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
            {{ $t('faq.quickActions') }}
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
                  {{ $t('faq.takeTest') }}
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
                  {{ $t('faq.viewResults') }}
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
                  {{ $t('faq.myProfile') }}
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
                  {{ $t('faq.createAccount') }}
                </v-btn>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>

        <!-- Still Need Help Section -->
        <v-card elevation="3" class="help-card">
          <v-row no-gutters>
            <v-col cols="12" md="8" class="pa-6">
              <h2 class="text-h5 font-weight-bold mb-3">{{ $t('faq.stillNeedHelp') }}</h2>
              <p class="text-body-1 mb-4">{{ $t('faq.stillNeedHelpDesc') }}</p>
              <div class="d-flex flex-wrap gap-3">
                <v-btn
                  color="primary"
                  size="large"
                  prepend-icon="mdi-robot"
                  @click="openChatbot"
                >
                  {{ $t('faq.chatWithAssistant') }}
                </v-btn>
                <v-btn
                  variant="outlined"
                  size="large"
                  prepend-icon="mdi-email"
                  href="mailto:chungsin.ipbi@gmail.com"
                >
                  {{ $t('faq.emailSupport') }}
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
      categoryDefinitions: [
        { id: 'getting-started', nameKey: 'faq.categories.gettingStarted', icon: 'mdi-rocket-launch', color: 'primary' },
        { id: 'career-test', nameKey: 'faq.categories.careerTest', icon: 'mdi-clipboard-list', color: 'orange' },
        { id: 'results', nameKey: 'faq.categories.results', icon: 'mdi-chart-bar', color: 'success' },
        { id: 'account', nameKey: 'faq.categories.account', icon: 'mdi-account-cog', color: 'info' },
        { id: 'career-guidance', nameKey: 'faq.categories.careerGuidance', icon: 'mdi-briefcase', color: 'purple' }
      ],
      faqDefinitions: [
        { id: 1, category: 'getting-started', qKey: 'faq.q1', aKey: 'faq.a1' },
        { id: 2, category: 'getting-started', qKey: 'faq.q2', aKey: 'faq.a2' },
        { id: 3, category: 'getting-started', qKey: 'faq.q3', aKey: 'faq.a3' },
        { id: 4, category: 'getting-started', qKey: 'faq.q4', aKey: 'faq.a4' },
        { id: 5, category: 'career-test', qKey: 'faq.q5', aKey: 'faq.a5' },
        { id: 6, category: 'career-test', qKey: 'faq.q6', aKey: 'faq.a6' },
        { id: 7, category: 'career-test', qKey: 'faq.q7', aKey: 'faq.a7' },
        { id: 8, category: 'career-test', qKey: 'faq.q8', aKey: 'faq.a8' },
        { id: 9, category: 'results', qKey: 'faq.q9', aKey: 'faq.a9' },
        { id: 10, category: 'results', qKey: 'faq.q10', aKey: 'faq.a10' },
        { id: 11, category: 'results', qKey: 'faq.q11', aKey: 'faq.a11' },
        { id: 12, category: 'results', qKey: 'faq.q12', aKey: 'faq.a12' },
        { id: 13, category: 'account', qKey: 'faq.q13', aKey: 'faq.a13' },
        { id: 14, category: 'account', qKey: 'faq.q14', aKey: 'faq.a14' },
        { id: 15, category: 'account', qKey: 'faq.q15', aKey: 'faq.a15' },
        { id: 16, category: 'account', qKey: 'faq.q16', aKey: 'faq.a16' },
        { id: 17, category: 'career-guidance', qKey: 'faq.q17', aKey: 'faq.a17' },
        { id: 18, category: 'career-guidance', qKey: 'faq.q18', aKey: 'faq.a18' },
        { id: 19, category: 'career-guidance', qKey: 'faq.q19', aKey: 'faq.a19' },
        { id: 20, category: 'career-guidance', qKey: 'faq.q20', aKey: 'faq.a20' }
      ]
    }
  },
  computed: {
    translatedCategories() {
      return this.categoryDefinitions.map(cat => ({
        ...cat,
        name: this.$t(cat.nameKey)
      }))
    },
    translatedFaqs() {
      return this.faqDefinitions.map(faq => ({
        ...faq,
        question: this.$t(faq.qKey),
        answer: this.$t(faq.aKey)
      }))
    },
    filteredFaqs() {
      let result = this.translatedFaqs
      
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        result = result.filter(faq => 
          faq.question.toLowerCase().includes(query) ||
          faq.answer.toLowerCase().includes(query)
        )
      }
      
      if (this.selectedCategory) {
        result = result.filter(faq => faq.category === this.selectedCategory)
      }
      
      return result
    },
    categoriesWithFaqs() {
      return this.translatedCategories
        .map(category => ({
          ...category,
          faqs: this.filteredFaqs.filter(faq => faq.category === category.id)
        }))
        .filter(category => category.faqs.length > 0)
    }
  },
  methods: {
    getCategoryCount(categoryId) {
      return this.translatedFaqs.filter(faq => faq.category === categoryId).length
    },
    openChatbot() {
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
