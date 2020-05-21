<template>
  <div id="terms-content">
    <v-layout justify-center>
      <h3>{{ $t("agreement.title") }}</h3>
    </v-layout>
    <v-container id="terms-window">
      <v-textarea
        v-show="this.$i18n.locale==='ja'"
        v-model="termsTextJa"
        outlined
        no-resize
        readonly
        height="50vh"
      />
      <v-textarea
        v-show="this.$i18n.locale==='en'"
        v-model="termsTextEn"
        outlined
        no-resize
        readonly
        height="50vh"
      />
    </v-container>
    <v-layout justify-center>
      <div>{{ $t("agreement.text") }}</div>
    </v-layout>
    <v-layout justify-center>
      <router-link
        to="/"
        class="agree-btn"
      >
        <v-btn text>
          {{ $t("agreement.notAgree") }}
        </v-btn>
      </router-link>
      <router-link
        to="/signup"
        class="agree-btn"
      >
        <v-btn color="primary">
          {{ $t("agreement.agree") }}
        </v-btn>
      </router-link>
    </v-layout>
  </div>
</template>

<script>
export default {
  name: 'AgreementView',
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
a {
    text-decoration: none;
}
#terms-content {
    margin-top: 70px;
}
#terms-window {
    height: 55vh;
}
.agree-btn {
    margin: 10px;
}
</style>
