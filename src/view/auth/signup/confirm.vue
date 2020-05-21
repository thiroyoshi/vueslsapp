<template>
  <div id="confirm-content">
    <v-layout justify-center>
      <Confirm />
    </v-layout>
    <v-layout justify-center>
      <router-link to="/">
        <v-btn
          id="back-btn"
          text
          small
        >
          <v-icon id="back-icon">
            fa-arrow-left
          </v-icon>{{ $t("confirm.toHome") }}
        </v-btn>
      </router-link>
    </v-layout>
  </div>
</template>

<script>
import Confirm from '../../../components/auth/confirm'

export default {
  name: 'ConfirmView',
  components: {
    Confirm
  }
}
</script>

<style scoped>
a {
  text-decoration: none;
}
#back-icon {
  margin-right: 10px;
  font-size: 10px;
}
#back-btn {
  margin-top: 20px;
}
#confirm-content {
  margin-top: 50px;
}
</style>
