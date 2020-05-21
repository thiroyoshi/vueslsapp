<template>
  <v-container id="about-content">
    <h2>{{ $t("about.title") }}</h2>
    <v-divider />
    <div>
      {{ $t("about.text") }}
    </div>
  </v-container>
</template>

<script>
export default {
  name: 'About'
}
</script>

<style scoped>
#about-content {
  margin-top: 40px;
  margin-bottom: 40px;
}
</style>
