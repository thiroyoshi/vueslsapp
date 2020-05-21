<template>
  <v-app>
    <GlobalHeader :title="title" />
    <div id="content">
      <router-view />
    </div>
    <GlobalFooter
      @change-locale-to-ja="changeLocaleToJa"
      @change-locale-to-en="changeLocaleToEn"
    />
  </v-app>
</template>

<script>
import GlobalHeader from './components/commons/global-header'
import GlobalFooter from './components/commons/global-footer'

export default {
  name: 'App',

  components: {
    GlobalHeader,
    GlobalFooter
  },

  data: () => ({
    title: 'Vue + Serverless App'
  }),
  created: function () {
    this.$store.commit('setIsAuth')
  },
  methods: {
    changeLocaleToJa: function () {
      this.$i18n.locale = 'ja'
    },
    changeLocaleToEn: function () {
      this.$i18n.locale = 'en'
    }
  }
}
</script>

<style scoped>
#content {
  margin-top: 28px;
}
</style>
