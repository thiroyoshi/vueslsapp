<template>
  <div id="reset-content">
    <v-layout justify-center>
      <Forgot />
    </v-layout>
    <v-layout justify-center>
      <router-link to="/">
        <v-btn
          id="back-btn"
          text
          small
        >
          <v-icon id="back-icon">
            fa-arrow-left
          </v-icon>{{ $t("forgot.toHome") }}
        </v-btn>
      </router-link>
    </v-layout>
  </div>
</template>

<script>
import Forgot from '../../../components/auth/forgot'

export default {
  name: 'ForgotView',
  components: {
    Forgot
  }
}
</script>

<style scoped>
a {
  text-decoration: none;
}
#back-icon {
    margin-right: 10px;
    font-size: 10px;
}
#back-btn {
    margin-top: 10px;
}
</style>
