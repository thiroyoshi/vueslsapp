import Vue from "vue"
import Vuex from "vuex"

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
      isAuth: "",
      isRegistered: false,
      signupEmail: "",
      forgotEmail: "",
    },
    getters: {
      isAuth: state => state.isAuth,
      isRegistered: state => state.isRegistered,
      signupEmail: state => state.signupEmail,
      forgotEmail: state => state.forgotEmail
    },
    mutations: {
      setIsAuth: (state) => {
        state.isAuth = localStorage.hasOwnProperty('idToken');
      },
      setIsRegistered: (state) => {
        state.isRegistered = true;
      },
      clearIsRegistered: (state) => {
        state.isRegistered = false;
      },
      setSignupEmail: (state, email) => {
        state.signupEmail = email;
      },
      clearSignupEmail:(state) => {
        state.signupEmail = "";
      },
      setForgotEmail: (state, email) => {
        state.forgotEmail = email;
      },
      clearForgotEmail:(state) => {
        state.forgotEmail = "";
      },
    },
    actions: {},
    modules: {}
  });