<template>
  <v-container id="register-content">
    <h2>Register Profile</h2>
    <v-divider />
    <v-container>
      <v-card>
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title>Profile</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-divider />
        <v-form
          ref="registerForm"
          class="input-form"
        >
          <v-text-field
            v-model="profile.username"
            :rules="[rules.required, rules.max]"
            label="Username"
            :disabled="Loading"
            counter
            required
          />
          <v-btn
            color="primary"
            :disabled="Loading"
            @click="register"
          >
            Register
          </v-btn>
        </v-form>
      </v-card>
    </v-container>

    <v-dialog
      v-model="dialog"
      persistent
      max-width="500"
    >
      <v-card class="mx-auto">
        <v-card-title>API Request Failed</v-card-title>
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
  </v-container>
</template>

<script>
export default {
  name: 'RegisterView',
  data: function () {
    return {
      rules: {
        required: value => !!value || 'Required.',
        max: v => v.length <= 30 || 'Max 30 characters'
      },
      apiHeaders: {
        'Authorization': localStorage.idToken,
        'Content-Type': 'application/json'
      },
      profile: {
        username: '',
        email: ''
      },
      Loading: false,
      errorMessage: '',
      dialog: false
    }
  },
  created: function () {
    this.profile.email = this.$store.getters.signupEmail
  },
  methods: {
    register: function () {
      if (this.$refs.registerForm.validate()) {
        this.putUser()
      }
    },
    putUser: function () {
      var url = process.env.VUE_APP_API_ORIGIN + '/users'
      var config = {
        headers: this.apiHeaders,
        responseType: 'json'
      }
      this.Loading = true
      this.axios.put(url, this.profile, config)
      .then(res => {  // eslint-disable-line
          this.Loading = false
          this.$store.commit('clearSignupEmail')
          this.$router.replace('/home')
        })
        .catch(err => {
          this.Loading = false
          this.errorMessage = err.response.data.message
          this.dialog = true
        })
    }
  }
}
</script>

<style scoped>
a {
  text-decoration: none;
}
.input-form {
  padding-left: 20px;
  padding-right: 20px;
  padding-bottom: 20px;
}
#back-icon {
  margin-right: 10px;
  font-size: 10px;
}
#back-btn {
  margin-top: 20px;
}
#register-content {
  margin-top: 50px;
}
</style>
