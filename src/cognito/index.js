import Vue from 'vue'
import Cognito from './cognito'
import config from './config'

Vue.use(Cognito, config)

export default new Cognito()
