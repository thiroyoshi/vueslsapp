<template>
  <div id="forgot-content">
    
    <v-card class="forgot mx-auto">
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title>Forgot your password?</v-list-item-title>
          <v-list-item-subtitle>Input your email to reset password</v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
      <v-form ref="ForgotForm" id="input-form">
        <v-text-field
          :rules="[rules.required]"
          v-model="email"
          label="Email"
          required
        ></v-text-field>
        <v-layout justify-center>
          <v-btn class="primary" @click="forgotPassword">Reset Request</v-btn>
        </v-layout>
      </v-form>
    </v-card>

    <v-dialog v-model="dialog" persistent max-width="500">
      <v-card class="mx-auto">
        <v-card-title>Reset Request Failed</v-card-title>
        <v-card-text>{{ errorMessage }}</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1" text @click="dialog = false">OK</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    
  </div>
</template>

<script>
export default {
  name: 'Forgot',
  data () {
    return {
      rules: {
        required: value => !!value || 'Required.'
      },
      email: '',
      dialog: false,
      errorMessage: "",
    }
  },
  methods: {
    forgotPassword () {
      if (this.$refs.ForgotForm.validate()) {
        this.$cognito.forgotPassword(this.email)
          .then(result => { // eslint-disable-line
            this.$store.commit("setForgotEmail", this.email);
            this.$router.replace('/reset')
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
  padding-bottom: 20px;
}
#forgot-content {
    margin-top: 50px;
}
#forgot-alert {
    margin-top: 20px;
    margin-right: 20%;
    margin-left: 20%;
}
a {
  text-decoration: none;
}
</style>