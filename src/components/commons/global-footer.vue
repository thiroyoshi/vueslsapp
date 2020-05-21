<template>
  <div id="content">
    <v-footer
      absolute
      dark
    >
      <v-layout
        id="contentslist"
        justify-center
      >
        <router-link
          to="/about"
          class="footer-content"
        >
          {{ $t("footer.about") }}
        </router-link>
        <span>|</span>
        <router-link
          to="/terms"
          class="footer-content"
        >
          {{ $t("footer.terms") }}
        </router-link>
        <span>|</span>
        <router-link
          to="/privacy"
          class="footer-content"
        >
          {{ $t("footer.privacypolicy") }}
        </router-link>
        <span>|</span>
        <router-link
          to="/help"
          class="footer-content"
        >
          {{ $t("footer.help") }}
        </router-link>
      </v-layout>
      <v-card-text class="py-2 white--text text-center">
        <button
          class="locale-button"
          type="button"
          @click="changeLocaleToJa"
        >
          <flag iso="jp" />
        </button>
        <button
          class="locale-button"
          type="button"
          @click="changeLocaleToEn"
        >
          <flag iso="us" />
        </button>
      </v-card-text>
      <v-card-text class="py-2 white--text text-center">
        &copy; {{ new Date().getFullYear() }} thiroyoshi
      </v-card-text>
    </v-footer>
  </div>
</template>

<script>
export default {
  name: 'GlobalFooter',
  methods: {
    changeLocaleToJa: function () {
      this.$emit('change-locale-to-ja')
    },
    changeLocaleToEn: function () {
      this.$emit('change-locale-to-en')
    }
  }
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
.locale-button{
  margin-right: 5px;
  margin-left: 5px;
}
#contentslist{
  margin-bottom: 5px;
}
a {
  text-decoration: none;
}
</style>
