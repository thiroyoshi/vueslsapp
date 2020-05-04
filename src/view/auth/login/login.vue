<template>
  <div id="login-content">
    <v-layout justify-center>
      <Login />
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
          </v-icon>back to home
        </v-btn>
      </router-link>
    </v-layout>
  </div>
</template>

<script>
import Login from '../../../components/auth/login'

export default {
  name: 'LoginView',
  components: {
    Login
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
#login-content {
    margin-top: 50px;
}
</style>
