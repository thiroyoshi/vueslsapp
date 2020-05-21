<template>
  <v-container id="privacy-content">
    <h2>{{ $t("privacy.title") }}</h2>
    <v-divider />
    <div>
      {{ $t("privacy.text") }}
    </div>
  </v-container>
</template>

<script>
export default {
  name: 'Privacy'
}
</script>

<style scoped>
#privacy-content {
  margin-top: 40px;
  margin-bottom: 40px;
}
</style>
