<template>
  <div id="reset-content">
    <v-layout justify-center>
      <Reset />
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
import Reset from '../../../components/auth/reset'

export default {
  name: 'ResetView',
  components: {
    Reset
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
    margin-top: 10px;
}
</style>
