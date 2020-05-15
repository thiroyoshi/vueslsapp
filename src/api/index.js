import axios from 'axios'
import store from '../store'

const domain = process.env.VUE_APP_API_ORIGIN

var config = {
  headers: {
    'Authorization': localStorage.idToken,
    'Content-Type': 'application/json'
  },
  responseType: 'json'
}

const onSuccess = (resp) => {
  store.commit('setIsApiLoading', false)
  return Promise.resolve(resp.data)
}
const onError = () => {
  store.commit('setIsApiLoading', false)
  throw new Error('API error.')
}

export default {
  get: (path, params) => {
    var url = domain + path
    store.commit('setIsApiLoading', true)
    return axios.get(url, config).then(onSuccess).catch(onError)
  },
  post: (path, params) => {
    var url = domain + path
    store.commit('setIsApiLoading', true)
    return axios.post(url, params, config).then(onSuccess).catch(onError)
  },
  put: (path, params) => {
    var url = domain + path
    store.commit('setIsApiLoading', true)
    return axios.put(url, params, config).then(onSuccess).catch(onError)
  },
  delete: (path, params) => {
    var url = domain + path
    config.data = params
    store.commit('setIsApiLoading', true)
    return axios.delete(url, config).then(onSuccess).catch(onError)
  },
  setConfig: () => {
    config = {
      headers: {
        'Authorization': localStorage.idToken,
        'Content-Type': 'application/json'
      },
      responseType: 'json'
    }
  }
}
