import Vue from 'vue'
import Router from 'vue-router'
import store from '../store'

Vue.use(Router)

const requireAuth = (to, from, next) => {
  if (localStorage.hasOwnProperty('idToken')) {
    var base64Url = localStorage.getItem('idToken').split('.')[1]
    var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/')
    var jsonPayload = decodeURIComponent(atob(base64).split('').map(function (c) {
      return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)
    }).join(''))
    var jp = JSON.parse(jsonPayload)

    var expDate = new Date(jp.exp * 1000)
    var now = new Date()

    if (now < expDate) {
      next()
    } else {
      localStorage.clear()
      store.commit('setIsAuth')
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      })
    }
  } else {
    localStorage.clear()
    store.commit('setIsAuth')
    next({
      path: '/login',
      query: { redirect: to.fullPath }
    })
  }
}

const onlyFromAgreement = (to, from, next) => {
  if (from.path === '/agreement') {
    next()
  } else {
    next('/agreement')
  }
}

const loggedIn = (to, from, next) => {
  if (localStorage.hasOwnProperty('idToken')) {
    next('/home')
  } else {
    next()
  }
}

const requireRegistered = (to, from, next) => {
  next()
}

const routes = [
  { path: '/',
    name: 'landing',
    component: () => import('@/view/landing.vue')
  },
  {
    path: '/home',
    name: 'home',
    component: () => import('@/view/main/home.vue'),
    beforeEnter: requireAuth, requireRegistered
  },
  {
    path: '/settings',
    name: 'settings',
    component: () => import('@/view/main/settings.vue'),
    beforeEnter: requireAuth, requireRegistered
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/view/auth/login/login.vue'),
    beforeEnter: loggedIn
  },
  {
    path: '/agreement',
    name: 'agreement',
    component: () => import('@/view/auth/signup/agreement.vue'),
    beforeEnter: loggedIn
  },
  {
    path: '/signup',
    name: 'signup',
    component: () => import('@/view/auth/signup/signup.vue'),
    beforeEnter: onlyFromAgreement, loggedIn
  },
  {
    path: '/confirm',
    name: 'confirm',
    component: () => import('@/view/auth/signup/confirm.vue'),
    beforeEnter: loggedIn
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('@/view/auth/signup/register.vue')
  },
  {
    path: '/forgot',
    name: 'forgot',
    component: () => import('@/view/auth/reset-password/forgot.vue')
  },
  {
    path: '/reset',
    name: 'reset',
    component: () => import('@/view/auth/reset-password/reset.vue')
  },
  {
    path: '/about',
    name: 'about',
    component: () => import('@/view/sub/about.vue')
  },
  {
    path: '/terms',
    name: 'terms',
    component: () => import('@/view/sub/terms.vue')
  },
  {
    path: '/help',
    name: 'help',
    component: () => import('@/view/sub/help.vue')
  },
  {
    path: '/privacy',
    name: 'privacy',
    component: () => import('@/view/sub/privacy.vue')
  },
  {
    path: '*',
    name: 'notfound',
    component: () => import('@/view/error/notfound.vue')
  }
]

const router = new Router({
  mode: 'history',
  routes
})

export default router
