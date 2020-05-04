<template>
  <v-app>
    <GlobalHeader :title="title" />
    <div id="content">
      <router-view />
    </div>
    <GlobalFooter />
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
  }
}
</script>

<style scoped>
#content {
  margin-top: 28px;
}
</style>
