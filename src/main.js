import Vue from 'vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify'
import vueaxios from './plugins/axios'
import VueAnalytics from 'vue-analytics'
import VueI18n from 'vue-i18n'
import FlagIcon from 'vue-flag-icon'
import App from './App.vue'
import cognito from './cognito'

Vue.config.productionTip = false

Vue.use(VueI18n)
const i18n = new VueI18n({
  locale: 'en',
  messages: require('./assets/messages.json')
})
Vue.use(VueAnalytics, {
  id: process.env.VUE_APP_GOOGLE_ANALYTICS,
  router
})
Vue.use(FlagIcon)

new Vue({
  router,
  store,
  vuetify,
  vueaxios,
  i18n,
  cognito,
  render: h => h(App)
}).$mount('#app')
