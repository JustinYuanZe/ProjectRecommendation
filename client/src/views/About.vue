<template>
  <v-container class="py-4">
    <v-row justify="center">
      <v-col cols="12" md="8" lg="7">
        <div class="text-center mb-5">
          <h1 class="text-h5 font-weight-bold mb-2">{{ $t('about.title') }}</h1>
          <p class="text-body-2 text--secondary">{{ $t('about.subtitle') }}</p>
        </div>

        <v-card class="pa-4 mb-4" elevation="1">
          <v-card-title class="text-body-1 font-weight-bold pb-2">{{ $t('about.missionTitle') }}</v-card-title>
          <v-card-text class="text-body-2 pt-0">
            <p>{{ $t('about.missionText') }}</p>
          </v-card-text>
        </v-card>

        <v-card class="pa-4 mb-4" elevation="1">
          <v-card-title class="text-body-1 font-weight-bold pb-2">{{ $t('about.whatWeOfferTitle') }}</v-card-title>
          <v-card-text class="pt-0">
            <v-row dense>
              <v-col cols="6">
                <div class="feature-item mb-3">
                  <v-icon color="primary" size="24">mdi-clipboard-check-outline</v-icon>
                  <strong class="text-body-2 d-block mt-1">{{ $t('about.offer1Title') }}</strong>
                  <p class="text-caption text-grey mt-1 mb-0">{{ $t('about.offer1Desc') }}</p>
                </div>
              </v-col>
              <v-col cols="6">
                <div class="feature-item mb-3">
                  <v-icon color="primary" size="24">mdi-robot</v-icon>
                  <strong class="text-body-2 d-block mt-1">{{ $t('about.offer2Title') }}</strong>
                  <p class="text-caption text-grey mt-1 mb-0">{{ $t('about.offer2Desc') }}</p>
                </div>
              </v-col>
              <v-col cols="6">
                <div class="feature-item mb-3">
                  <v-icon color="primary" size="24">mdi-account-star</v-icon>
                  <strong class="text-body-2 d-block mt-1">{{ $t('about.offer3Title') }}</strong>
                  <p class="text-caption text-grey mt-1 mb-0">{{ $t('about.offer3Desc') }}</p>
                </div>
              </v-col>
              <v-col cols="6">
                <div class="feature-item mb-3">
                  <v-icon color="primary" size="24">mdi-school-outline</v-icon>
                  <strong class="text-body-2 d-block mt-1">{{ $t('about.offer4Title') }}</strong>
                  <p class="text-caption text-grey mt-1 mb-0">{{ $t('about.offer4Desc') }}</p>
                </div>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>

        <v-card class="pa-4 mb-4" elevation="1">
          <v-card-title class="text-body-1 font-weight-bold pb-2">{{ $t('about.teamTitle') }}</v-card-title>
          <v-card-text class="text-body-2 pt-0">
            <p class="mb-0">{{ $t('about.teamText') }}</p>
          </v-card-text>
        </v-card>

        <v-card class="pa-4" elevation="1">
          <v-card-title class="text-body-1 font-weight-bold pb-2">{{ $t('about.contactTitle') }}</v-card-title>
          <v-card-text class="pt-0">
            <p class="text-body-2 mb-2">{{ $t('about.contactText') }}</p>
            <p class="text-body-2 mb-0">
              <v-icon size="small" class="mr-1">mdi-email</v-icon>
              <strong>chungsin.ipbi@gmail.com</strong>
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
