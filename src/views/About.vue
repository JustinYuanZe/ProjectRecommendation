<template>
  <v-container class="py-8">
    <v-row justify="center">
      <v-col cols="12" md="8">
        <div class="text-center mb-8">
          <h1 class="text-h3 font-weight-bold mb-4">{{ $t('about.title') }}</h1>
          <p class="text-h6 text--secondary">{{ $t('about.subtitle') }}</p>
        </div>

        <v-card class="pa-6 mb-6" elevation="2">
          <v-card-title class="text-h5 mb-4">{{ $t('about.missionTitle') }}</v-card-title>
          <v-card-text class="text-body-1">
            <p class="mb-4">{{ $t('about.missionText') }}</p>
          </v-card-text>
        </v-card>

        <v-card class="pa-6 mb-6" elevation="2">
          <v-card-title class="text-h5 mb-4">{{ $t('about.whatWeOfferTitle') }}</v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12" md="6">
                <div class="feature-item mb-4">
                  <v-icon color="primary" class="mr-3" size="32">mdi-clipboard-check-outline</v-icon>
                  <strong>{{ $t('about.offer1Title') }}</strong>
                  <p class="mt-2 text-grey">{{ $t('about.offer1Desc') }}</p>
                </div>
              </v-col>
              <v-col cols="12" md="6">
                <div class="feature-item mb-4">
                  <v-icon color="primary" class="mr-3" size="32">mdi-robot</v-icon>
                  <strong>{{ $t('about.offer2Title') }}</strong>
                  <p class="mt-2 text-grey">{{ $t('about.offer2Desc') }}</p>
                </div>
              </v-col>
              <v-col cols="12" md="6">
                <div class="feature-item mb-4">
                  <v-icon color="primary" class="mr-3" size="32">mdi-account-star</v-icon>
                  <strong>{{ $t('about.offer3Title') }}</strong>
                  <p class="mt-2 text-grey">{{ $t('about.offer3Desc') }}</p>
                </div>
              </v-col>
              <v-col cols="12" md="6">
                <div class="feature-item mb-4">
                  <v-icon color="primary" class="mr-3" size="32">mdi-school-outline</v-icon>
                  <strong>{{ $t('about.offer4Title') }}</strong>
                  <p class="mt-2 text-grey">{{ $t('about.offer4Desc') }}</p>
                </div>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>

        <v-card class="pa-6 mb-6" elevation="2">
          <v-card-title class="text-h5 mb-4">{{ $t('about.teamTitle') }}</v-card-title>
          <v-card-text class="text-body-1">
            <p>{{ $t('about.teamText') }}</p>
          </v-card-text>
        </v-card>

        <v-card class="pa-6" elevation="2">
          <v-card-title class="text-h5 mb-4">{{ $t('about.contactTitle') }}</v-card-title>
          <v-card-text>
            <p class="mb-4">{{ $t('about.contactText') }}</p>
            <p class="mb-2">
              <v-icon class="mr-2">mdi-email</v-icon>
              <strong>{{ $t('about.contactEmail', { email: 'chungsin.ipbi@gmail.com' }) }}</strong>
            </p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'About'
}
</script>

<style scoped>
.feature-item {
  display: flex;
  align-items: flex-start;
  flex-direction: column;
}

.feature-item .v-icon {
  margin-bottom: 8px;
}
</style>
