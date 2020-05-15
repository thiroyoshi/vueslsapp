import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    isAuth: '',
    isRegistered: false,
    signupEmail: '',
    forgotEmail: '',
    isApiLoading: false
  },
  getters: {
    isAuth: state => state.isAuth,
    isRegistered: state => state.isRegistered,
    signupEmail: state => state.signupEmail,
    forgotEmail: state => state.forgotEmail,
    isApiLoading: state => state.isApiLoading
  },
  mutations: {
    setIsAuth: (state) => {
      state.isAuth = localStorage.hasOwnProperty('idToken')
    },
    setIsRegistered: (state, param) => {
      state.isRegistered = param
    },
    setSignupEmail: (state, email) => {
      state.signupEmail = email
    },
    clearSignupEmail: (state) => {
      state.signupEmail = ''
    },
    setForgotEmail: (state, email) => {
      state.forgotEmail = email
    },
    clearForgotEmail: (state) => {
      state.forgotEmail = ''
    },
    setIsApiLoading: (state, param) => {
      state.isApiLoading = param
    }
  },
  actions: {},
  modules: {}
})
