<template>
  <v-container id="home-content">
    <!-- GET -->
    <v-card raised>
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title>{{ $t("home.getApi.title") }}</v-list-item-title>
          <v-list-item-subtitle>{{ $t("home.getApi.subtitle") }}</v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
      <v-divider />
      <v-form class="input-form">
        <v-btn
          color="primary"
          :disabled="this.$store.getters.isApiLoading"
          @click="getMessage"
        >
          {{ $t("home.getApi.request") }}
        </v-btn>
        <v-progress-circular
          v-show="this.$store.getters.isApiLoading"
          class="api-loading"
          indeterminate
          size="20"
          width="3"
          color="primary"
        />
        <v-textarea
          v-model="getApiResult"
          class="api-result"
          outlined
          counter
          no-resize
          readonly
          :label="$t('home.getApi.result')"
        />
      </v-form>
    </v-card>
    <br>

    <!-- POST -->
    <v-card raised>
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title>{{ $t("home.postApi.title") }}</v-list-item-title>
          <v-list-item-subtitle>{{ $t("home.postApi.subtitle") }}</v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
      <v-divider />
      <v-form class="input-form">
        <v-text-field
          v-model="postApiBody.message"
          counter
          :label="$t('home.postApi.message')"
        />
        <v-btn
          color="primary"
          :disabled="this.$store.getters.isApiLoading"
          @click="postMessage"
        >
          {{ $t("home.postApi.request") }}
        </v-btn>
        <v-progress-circular
          v-show="this.$store.getters.isApiLoading"
          class="api-loading"
          indeterminate
          size="20"
          width="3"
          color="primary"
        />
        <v-textarea
          v-model="postApiResult"
          class="api-result"
          outlined
          counter
          no-resize
          readonly
          :label="$t('home.postApi.result')"
        />
      </v-form>
    </v-card>
    <br>

    <!-- PUT -->
    <v-card raised>
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title>{{ $t("home.putApi.title") }}</v-list-item-title>
          <v-list-item-subtitle>{{ $t("home.putApi.subtitle") }}</v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
      <v-divider />
      <v-form class="input-form">
        <v-text-field
          v-model="putApiBody.message"
          counter
          :label="$t('home.putApi.message')"
        />
        <v-text-field
          v-model="putApiBody.message_id"
          counter
          :label="$t('home.putApi.messageId')"
        />
        <v-btn
          color="primary"
          :disabled="this.$store.getters.isApiLoading"
          @click="putMessage"
        >
          {{ $t("home.putApi.request") }}
        </v-btn>
        <v-progress-circular
          v-show="this.$store.getters.isApiLoading"
          class="api-loading"
          indeterminate
          size="20"
          width="3"
          color="primary"
        />
        <v-textarea
          v-model="putApiResult"
          class="api-result"
          outlined
          counter
          no-resize
          readonly
          :label="$t('home.putApi.result')"
        />
      </v-form>
    </v-card>
    <br>

    <!-- DELETE -->
    <v-card raised>
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title>{{ $t("home.deleteApi.title") }}</v-list-item-title>
          <v-list-item-subtitle>{{ $t("home.deleteApi.subtitle") }}</v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
      <v-divider />
      <v-form class="input-form">
        <v-text-field
          v-model="deleteApiBody.message_id"
          counter
          :label="$t('home.deleteApi.messageId')"
        />
        <v-btn
          color="primary"
          :disabled="this.$store.getters.isApiLoading"
          @click="deleteMessage"
        >
          {{ $t("home.deleteApi.request") }}
        </v-btn>
        <v-progress-circular
          v-show="this.$store.getters.isApiLoading"
          class="api-loading"
          indeterminate
          size="20"
          width="3"
          color="primary"
        />
        <v-textarea
          v-model="deleteApiResult"
          class="api-result"
          outlined
          counter
          no-resize
          readonly
          :label="$t('home.deleteApi.result')"
        />
      </v-form>
    </v-card>

    <v-dialog
      v-model="dialog"
      persistent
      max-width="500"
    >
      <v-card>
        <v-card-title>{{ $t("home.dialog.title") }}</v-card-title>
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
import API from '../../api'

export default {
  name: 'Home',
  data: function () {
    return {
      getApiResult: '',
      postApiResult: '',
      putApiResult: '',
      deleteApiResult: '',
      postApiBody: {
        message: ''
      },
      putApiBody: {
        message_id: '', // eslint-disable-line
        message: ''
      },
      deleteApiBody: {
        message_id: '' // eslint-disable-line
      },
      errorMessage: '',
      dialog: false
    }
  },
  methods: {
    getMessage: function () {
      API.get('/messages', null)
        .then(res => {
          this.getApiResult = JSON.stringify(res.messages, null, '\t')
        })
        .catch(err => {
          this.errorMessage = err.message
          this.dialog = true
        })
    },
    postMessage: function () {
      API.post('/messages', this.postApiBody)
        .then(res => {
          this.postApiResult = JSON.stringify(res.message, null, '\t')
        })
        .catch(err => {
          this.errorMessage = err.message
          this.dialog = true
        })
    },
    putMessage: function () {
      API.put('/messages', this.putApiBody)
        .then(res => {
          this.putApiResult = JSON.stringify(res.message, null, '\t')
        })
        .catch(err => {
          this.errorMessage = err.message
          this.dialog = true
        })
    },
    deleteMessage: function () {
      API.delete('/messages', this.deleteApiBody)
        .then(res => {
          this.deleteApiResult = JSON.stringify(res.message, null, '\t')
        })
        .catch(err => {
          this.errorMessage = err.message
          this.dialog = true
        })
    }
  }
}
</script>

<style scoped>
#home-content {
  margin-top: 40px;
  margin-bottom: 90px;
}
.input-form {
  padding-top: 20px;
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
