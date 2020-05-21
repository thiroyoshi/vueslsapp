<template>
  <div id="signup-content">
    <v-card class="signup mx-auto">
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title>{{ $t("signup.title") }}</v-list-item-title>
          <v-list-item-subtitle>{{ $t("signup.subtitle") }}</v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
      <v-form
        id="input-form"
        ref="signupForm"
      >
        <v-text-field
          v-model="email"
          :rules="[rules.required]"
          :label="$t('signup.email')"
          required
        />
        <v-text-field
          v-model="password"
          :rules="[rules.required, rules.min]"
          :label="$t('signup.password')"
          type="password"
          autocomplete="new-password"
          required
        />
        <v-text-field
          v-model="passwordConfirm"
          :rules="[rules.required, rules.min]"
          :label="$t('signup.passwordConfirm')"
          type="password"
          autocomplete="new-password"
          required
        />
        <v-layout justify-center>
          <v-btn
            class="primary"
            @click="singup"
          >
            {{ $t("signup.signup") }}
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
        <v-card-title>{{ $t("signup.dialog.title") }}</v-card-title>
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
  name: 'Signup',
  data () {
    return {
      rules: {
        required: value => !!value || 'Required.',
        min: v => v.length >= 8 || 'Min 8 characters'
      },
      email: '',
      password: '',
      passwordConfirm: '',
      dialog: false,
      errorMessage: ''
    }
  },
  methods: {
    singup () {
      if (this.$refs.signupForm.validate()) {
        if (this.email && (this.password === this.passwordConfirm)) {
          this.$cognito.signUp(this.email, this.password)
            .then(result => { // eslint-disable-line
              this.$store.commit('setSignupEmail', this.email)
              this.$router.replace('/confirm')
            })
            .catch(err => {
              this.errorMessage = err.message
              this.dialog = true
            })
        }
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
a {
  text-decoration: none;
}
</style>
