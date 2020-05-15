<template>
  <div id="signup-content">
    <v-card class="login mx-auto">
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title>Login</v-list-item-title>
          <v-list-item-subtitle>Input your email and password to login</v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
      <v-form
        id="input-form"
        ref="loginForm"
      >
        <v-text-field
          v-model="email"
          :rules="[rules.required]"
          label="Email"
          autocomplete="username"
          required
        />
        <v-text-field
          v-model="password"
          :rules="[rules.required, rules.min]"
          label="Password"
          type="password"
          autocomplete="current-password"
          required
        />
        <v-layout justify-center>
          <v-btn
            class="primary"
            @click="login"
          >
            Login
          </v-btn>
          <router-link to="/agreement">
            <v-btn
              text
              color="accent-4"
            >
              Signup
            </v-btn>
          </router-link>
        </v-layout>
      </v-form>
      <v-divider />
      <v-card-actions>
        <router-link to="/forgot">
          <v-btn
            text
            small
            color="warning"
          >
            Forgot Password?
          </v-btn>
        </router-link>
      </v-card-actions>
    </v-card>

    <v-dialog
      v-model="dialog"
      persistent
      max-width="500"
    >
      <v-card class="mx-auto">
        <v-card-title>Login Failed</v-card-title>
        <v-card-text>{{ errorMessage }}</v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn
            color="green darken-1"
            text
            @click="dialog = false"
          >
            OK
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import API from '../../api'

export default {
  name: 'Login',
  data () {
    return {
      apiHeaders: {
        'Authorization': localStorage.idToken,
        'Content-Type': 'application/json'
      },
      email: '',
      password: '',
      rules: {
        required: value => !!value || 'Required.',
        min: v => v.length >= 8 || 'Min 8 characters'
      },
      dialog: false,
      errorMessage: ''
    }
  },
  methods: {
    login () {
      if (this.$refs.loginForm.validate()) {
        this.$cognito.login(this.email, this.password)
          .then(result => {
            localStorage.setItem('idToken', result.idToken.jwtToken)
            localStorage.setItem('refreshToken', result.refreshToken.token)
            localStorage.setItem('accessToken', result.accessToken.jwtToken)
            localStorage.setItem('payload', JSON.stringify(result.idToken.payload))
            localStorage.setItem('userId', result.idToken.payload['cognito:username'])
            this.$store.commit('setIsAuth')

            API.setConfig()
            API.get('/users', null)
              .then(res => {
                console.log(res)
                if (res.data.username === res.data.cognito_user_id) {
                  this.$store.commit('setSignupEmail', this.email)
                  this.$store.commit('setIsRegistered', false)
                  this.$router.replace('/register')
                } else {
                  this.$store.commit('setIsRegistered', true)
                  this.$router.replace('/home')
                }
              })
              .catch(err => { // eslint-disable-line
                this.$store.commit('setIsRegistered', false)
                this.$router.replace('/register')
              })
          })
          .catch(err => {
            this.errorMessage = err.message
            this.dialog = true
          })
      }
    }
  }
}
</script>

<style scoped>
#input-form {
  padding-left: 20px;
  padding-right: 20px;
  margin-bottom: 20px;
}
a {
  text-decoration: none;
}
</style>
