<template>
  <div id="terms-content">
    <v-layout justify-center>
      <h3>Terms and Conditions</h3>
    </v-layout>
    <v-container id="terms-window">
      <v-textarea
        v-model="termsText"
        outlined
        no-resize
        readonly
        height="50vh"
      />
    </v-container>
    <v-layout justify-center>
      <div>Do you agree with the terms and conditions?</div>
    </v-layout>
    <v-layout justify-center>
      <router-link
        to="/"
        class="agree-btn"
      >
        <v-btn text>
          Not Agree
        </v-btn>
      </router-link>
      <router-link
        to="/signup"
        class="agree-btn"
      >
        <v-btn color="primary">
          I Agree
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
