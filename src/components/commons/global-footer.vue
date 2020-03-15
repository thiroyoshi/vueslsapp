<template>
  <div id="content">
    <v-footer absolute dark>
      <v-layout justify-center>
        <router-link to="/about" class="footer-content">About</router-link>
        <span>|</span>
        <router-link to="/terms" class="footer-content">Terms</router-link>
        <span>|</span>
        <router-link to="/privacy" class="footer-content">Privacy Policy</router-link>
        <span>|</span>
        <router-link to="/help" class="footer-content">Help</router-link>
      </v-layout>
      <v-card-text class="py-2 white--text text-center">
        &copy; {{ new Date().getFullYear() }} thiroyoshi
      </v-card-text>
    </v-footer>
  </div>
</template>

<script>
export default {
    name: 'global-footer',
}
</script>

<style scoped>
.footer-content{
  margin-top: 5px;
  margin-right: 10px;
  margin-left: 10px;
  font-size: 13px;
  color: #EEE;
}
a {
  text-decoration: none;
}
</style>