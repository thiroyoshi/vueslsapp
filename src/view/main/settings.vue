<template>
  <v-container id="home-content">
    <h2>Settings</h2>
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
          ref="profileForm"
          class="input-form"
        >
          <v-text-field
            v-model="profile.username"
            :rules="[rules.required, rules.max]"
            label="Username"
            :disabled="this.$store.getters.isApiLoading"
            counter
            required
          />
          <v-text-field
            v-model="profile.email"
            :rules="[rules.required]"
            label="E-mail"
            :disabled="this.$store.getters.isApiLoading"
            required
          />
          <v-btn
            color="primary"
            :disabled="this.$store.getters.isApiLoading"
            @click="updateProfile"
          >
            Update
          </v-btn>
        </v-form>
      </v-card>
      <br>
      <v-card>
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title>Password</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-divider />
        <v-form
          ref="passwordForm"
          class="input-form"
        >
          <v-text-field
            v-model="oldPassword"
            :rules="[rules.required, rules.min]"
            :disabled="this.$store.getters.isApiLoading"
            label="Old Password"
            type="password"
            autocomplete="current-password"
            required
          />
          <v-text-field
            v-model="password"
            :rules="[rules.required, rules.min]"
            :disabled="this.$store.getters.isApiLoading"
            label="New Password"
            type="password"
            autocomplete="new-password"
            required
          />
          <v-text-field
            v-model="passwordConfirm"
            :disabled="this.$store.getters.isApiLoading"
            :rules="[rules.required, rules.min]"
            label="New Password(Confirm)"
            type="password"
            autocomplete="new-password"
            required
          />
          <v-btn
            color="primary"
            :disabled="this.$store.getters.isApiLoading"
            @click="updatePassword"
          >
            Update
          </v-btn>
        </v-form>
      </v-card>
      <br>
      <v-card>
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title id="delete-title">
              Delete Account
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-divider />
        <v-form class="input-form">
          <v-alert
            dense
            outlined
            type="error"
          >
            Make sure that you want to delete your <strong>ALL DATA</strong>.
          </v-alert>
          <v-btn
            id="delete-btn"
            :disabled="this.$store.getters.isApiLoading"
            @click="deleteDialog = true"
          >
            Delete
          </v-btn>
        </v-form>
      </v-card>
    </v-container>

    <!-- Dialog for Password Changed -->
    <v-dialog
      v-model="passwordDialog"
      persistent
      max-width="500"
    >
      <v-card>
        <v-card-title>Password Changed Successfuly</v-card-title>
        <v-card-actions>
          <v-spacer />
          <v-btn
            color="green darken-1"
            text
            @click="passwordDialog = false"
          >
            OK
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Dialog for Password Validation -->
    <v-dialog
      v-model="passwordErrorDialog"
      persistent
      max-width="500"
    >
      <v-card class="mx-auto">
        <v-card-title>Password Validation Failed</v-card-title>
        <v-card-text>Your new passwords are not match.</v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn
            color="green darken-1"
            text
            @click="passwordErrorDialog = false"
          >
            OK
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Dialog for Delete Confirmation -->
    <v-dialog
      v-model="deleteDialog"
      persistent
      max-width="500"
    >
      <v-card class="mx-auto">
        <v-card-title>Are you sure to delete the account?</v-card-title>
        <v-card-text>All your data will be deleted.</v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn
            color="green darken-1"
            text
            @click="deleteDialog = false"
          >
            Cancel
          </v-btn>
          <v-btn
            color="error"
            @click="deleteAccount"
          >
            Delete
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Dialog for API Failed -->
    <v-dialog
      v-model="errorDialog"
      persistent
      max-width="500"
    >
      <v-card class="mx-auto">
        <v-card-title>Settings API Request Failed</v-card-title>
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
  </v-container>
</template>

<script>
import API from '../../api'

export default {
  name: 'Settings',
  data: function () {
    return {
      rules: {
        required: value => !!value || 'Required.',
        min: v => v.length >= 8 || 'Min 8 characters',
        max: v => v.length <= 30 || 'Max 30 characters'
      },
      apiHeaders: {
        'Authorization': localStorage.idToken,
        'Content-Type': 'application/json'
      },
      profile: {
        userId: '',
        username: '',
        email: ''
      },
      oldPassword: '',
      password: '',
      passwordConfirm: '',
      passwordDialog: false,
      passwordErrorDialog: false,
      deleteDialog: false,
      errorMessage: '',
      errorDialog: false
    }
  },
  created: function () {
    this.getUser()
  },
  methods: {
    updateProfile: function () {
      if (this.$refs.profileForm.validate()) {
        this.putUser()
      }
    },
    updatePassword: function () {
      if (this.$refs.passwordForm.validate()) {
        if (this.oldPassword && (this.password === this.passwordConfirm)) {
          this.$cognito.changePassword(this.oldPassword, this.password)
                    .then(result => {   // eslint-disable-line
              this.passwordDialog = true
            })
            .catch(err => {
              this.errorMessage = err.message
              this.errorDialog = true
            })
        } else {
          this.passwordErrorDialog = true
        }
      }
    },
    deleteAccount: function () {
      this.$cognito.delete()
            .then(result => { // eslint-disable-line
          localStorage.clear()
          this.$store.commit('setIsAuth')
          this.$router.replace('/')
          this.deleteDialog = false
        })
        .catch(err => {
          this.errorMessage = err.message
          this.errorDialog = true
        })
    },
    getUser: function () {
      API.get('/users', null)
        .then(res => {
          this.profile.userId = res.data.userId
          this.profile.username = res.data.username
          this.profile.email = res.data.email
        })
        .catch(err => {
          this.errorMessage = err.message
          this.errorDialog = true
        })
    },
    putUser: function () {
      API.post('/users', this.profile)
        .then(res => {
          console.log(res)
        })
        .catch(err => {
          this.errorMessage = err.response.data.message
          this.errorDialog = true
        })
    }
  }
}
</script>

<style scoped>
#home-content {
  margin-top: 40px;
  margin-bottom: 40px;
}
#delete-title {
    color:red;
}
#delete-btn {
    color:red;
}
.input-form {
  padding-top: 10px;
  padding-bottom: 20px;
  padding-left: 20px;
  padding-right: 20px;
}
.api-loading {
    margin-left:10px;
}
.api-result {
    margin-top: 15px;
    font-size: 14px;
}
a {
  text-decoration: none;
}
</style>
