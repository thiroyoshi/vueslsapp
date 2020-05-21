<template>
  <div id="reset-content">
    <v-card class="reset mx-auto">
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title>{{ $t("reset.title") }}</v-list-item-title>
          <v-list-item-subtitle>{{ $t("reset.subtitle") }}</v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
      <v-form
        id="input-form"
        ref="ResetForm"
      >
        <v-text-field
          v-model="email"
          :rules="[rules.required]"
          :label="$t('reset.email')"
          readonly
          required
        />
        <v-text-field
          v-model="verificationCode"
          :rules="[rules.required, rules.equal]"
          :label="$t('reset.verificationCode')"
          required
        />
        <v-text-field
          v-model="password"
          :rules="[rules.required, rules.min]"
          :label="$t('reset.password')"
          type="password"
          autocomplete="new-password"
          required
        />
        <v-text-field
          v-model="passwordConfirm"
          :rules="[rules.required, rules.min]"
          :label="$t('reset.passwordConfirm')"
          type="password"
          autocomplete="new-password"
          required
        />
        <v-layout justify-center>
          <v-btn
            class="primary"
            @click="resetPassword"
          >
            {{ $t("reset.reset") }}
          </v-btn>
        </v-layout>
      </v-form>
    </v-card>

    <v-dialog
      v-model="successDialog"
      persistent
      max-width="500"
    >
      <v-card class="mx-auto">
        <v-card-title>{{ $t("reset.dialog.title") }}</v-card-title>
        <v-card-text>{{ $t("reset.dialog.text") }}</v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn
            color="green darken-1"
            text
            @click="goToLoginView"
          >
            OK
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog
      v-model="errorDialog"
      persistent
      max-width="500"
    >
      <v-card class="mx-auto">
        <v-card-title>{{ $t("reset.errorDialog.title") }}</v-card-title>
        <v-card-text>{{ errorMessage }}</v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn
            color="green darken-1"
            text
            @click="errorDialog = false"
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
  name: 'Reset',
  data () {
    return {
      rules: {
        required: value => !!value || 'Required.',
        min: v => v.length >= 8 || 'Min 8 characters',
        equal: v => v.length === 6 || 'Equals 6 characters'
      },
      email: '',
      verificationCode: '',
      password: '',
      passwordConfirm: '',
      successDialog: false,
      errorDialog: false,
      errorMessage: ''
    }
  },
  created: function () {
    this.email = this.$store.getters.forgotEmail
  },
  methods: {
    resetPassword () {
      if (this.$refs.ResetForm.validate()) {
        this.$cognito.confirmForgotPassword(this.email, this.verificationCode, this.password)
          .then(result => { // eslint-disable-line
            this.$store.commit('clearSignupEmail')
            this.successDialog = true
          })
          .catch(err => {
            this.errorMessage = err.message
            this.dialog = true
          })
      }
    },
    goToLoginView () {
      this.successDialog = false
      this.$router.replace('/login')
    }
  }
}
</script>

<style scoped>
a {
  text-decoration: none;
}
#input-form {
  padding-left: 20px;
  padding-right: 20px;
  padding-bottom: 20px;
}
#reset-content {
    margin-top: 50px;
}
#reset-alert {
    margin-top: 20px;
    margin-right: 20%;
    margin-left: 20%;
}
</style>
