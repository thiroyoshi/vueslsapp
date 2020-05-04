<template>
  <v-container id="terms-content">
    <h2>Terms and Conditions</h2>
    <v-divider />
    <v-container id="terms-window">
      <v-textarea
        v-model="termsText"
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
      termsText: ''
    }
  },
  mounted: function () {
    this.axios.get('terms.txt')
      .then(res => {
        this.termsText = res.data
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
