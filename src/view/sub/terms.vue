<template>
  <v-container id="terms-content">
    <h2>{{ $t("terms.title") }}</h2>
    <v-divider />
    <v-container id="terms-window">
      <v-textarea
        v-show="this.$i18n.locale==='ja'"
        v-model="termsTextJa"
        outlined
        no-resize
        readonly
        height="60vh"
      />
      <v-textarea
        v-show="this.$i18n.locale==='en'"
        v-model="termsTextEn"
        outlined
        no-resize
        readonly
        height="60vh"
      />
    </v-container>
  </v-container>
</template>

<script>
export default {
  name: 'Terms',
  data: function () {
    return {
      termsTextJa: '',
      termsTextEn: ''
    }
  },
  mounted: function () {
    this.axios.get('ja/terms.txt')
      .then(res => {
        this.termsTextJa = res.data
      })
    this.axios.get('en/terms.txt')
      .then(res => {
        this.termsTextEn = res.data
      })
  }

}
</script>

<style scoped>
#terms-content {
  margin-top: 40px;
  margin-bottom: 40px;
}
</style>
