<template>
  <v-container id="help-content">
    <h2>{{ $t("help.title") }}</h2>
    <v-divider />
    <div>
      {{ $t("help.text") }}
    </div>
  </v-container>
</template>

<script>
export default {
  name: 'Help'
}
</script>

<style scoped>
#help-content {
  margin-top: 40px;
  margin-bottom: 40px;
}
</style>
