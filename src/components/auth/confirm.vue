<template>
  <div id="signup-content">
    <v-alert type="info">
      {{ $t("confirm.alert") }}
    </v-alert>

    <v-card class="signup mx-auto">
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title>{{ $t("confirm.title") }}</v-list-item-title>
          <v-list-item-subtitle>{{ $t("confirm.subtitle") }}</v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
      <v-form
        id="input-form"
        ref="confirmForm"
      >
        <v-text-field
          v-model="email"
          :label="$t('confirm.email')"
          readonly
          required
        />
        <v-text-field
          v-model="verificationCode"
          :rules="[rules.required, rules.equal]"
          :label="$t('confirm.verificationCode')"
          required
        />
        <v-layout justify-center>
          <v-btn
            class="primary"
            @click="confirm"
          >
            {{ $t("confirm.confirm") }}
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
        <v-card-title>{{ $t("confirm.successDialog.title") }}</v-card-title>
        <v-card-text>{{ $t("confirm.successDialog.text") }}</v-card-text>
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
        <v-card-title>{{ $t("confirm.errorDialog.title") }}</v-card-title>
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
  name: 'Confirm',
  data () {
    return {
      rules: {
        required: value => !!value || 'Required.',
        equal: v => v.length === 6 || 'Equals 6 characters'
      },
      email: '',
      verificationCode: '',
      successDialog: false,
      errorDialog: false,
      errorMessage: ''
    }
  },
  created: function () {
    this.email = this.$store.getters.signupEmail
  },
  methods: {
    confirm () {
      if (this.$refs.confirmForm.validate()) {
        this.$cognito.confirmation(this.email, this.verificationCode)
          .then(result => { // eslint-disable-line
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
#input-form {
  padding-left: 20px;
  padding-right: 20px;
  padding-bottom: 20px;
}
a {
  text-decoration: none;
}
</style>
