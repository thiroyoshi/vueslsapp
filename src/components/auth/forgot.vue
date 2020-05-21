<template>
  <div id="forgot-content">
    <v-card class="forgot mx-auto">
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title>{{ $t("forgot.title") }}</v-list-item-title>
          <v-list-item-subtitle>{{ $t("forgot.subtitle") }}</v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
      <v-form
        id="input-form"
        ref="ForgotForm"
      >
        <v-text-field
          v-model="email"
          :rules="[rules.required]"
          :label="$t('forgot.email')"
          required
        />
        <v-layout justify-center>
          <v-btn
            class="primary"
            @click="forgotPassword"
          >
            {{ $t("forgot.request") }}
          </v-btn>
        </v-layout>
      </v-form>
    </v-card>

    <v-dialog
      v-model="dialog"
      persistent
      max-width="500"
    >
      <v-card class="mx-auto">
        <v-card-title>{{ $t("forgot.dialog.title") }}</v-card-title>
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
export default {
  name: 'Forgot',
  data () {
    return {
      rules: {
        required: value => !!value || 'Required.'
      },
      email: '',
      dialog: false,
      errorMessage: ''
    }
  },
  methods: {
    forgotPassword () {
      if (this.$refs.ForgotForm.validate()) {
        this.$cognito.forgotPassword(this.email)
          .then(result => { // eslint-disable-line
            this.$store.commit('setForgotEmail', this.email)
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
