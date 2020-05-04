import Vue from 'vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify'
import vueaxios from './plugins/axios'
import VueAnalytics from 'vue-analytics'
import App from './App.vue'
import cognito from './cognito'

Vue.config.productionTip = false

new Vue({
  router,
  store,
  vuetify,
  vueaxios,
  cognito,
  render: h => h(App)
}).$mount('#app')

Vue.use(VueAnalytics, {
  id: process.env.VUE_APP_GOOGLE_ANALYTICS,
  router
})
