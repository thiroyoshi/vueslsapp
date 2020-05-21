<template>
  <div id="content">
    <v-container
      id="banner"
      fluid
    >
      <v-layout justify-center>
        <h3>{{ $t("landing.title") }}</h3>
      </v-layout>
    </v-container>
    <v-container>
      <v-row
        class="mb-6"
        justify="center"
        no-gutters
      >
        <div class="pa-3">
          <router-link
            to="/login"
          >
            <v-btn color="primary">
              {{ $t("landing.login") }}
            </v-btn>
          </router-link>
        </div>
        <div class="pa-3">
          <router-link
            to="/agreement"
          >
            <v-btn color="primary">
              {{ $t("landing.signup") }}
            </v-btn>
          </router-link>
        </div>
      </v-row>
    </v-container>
  </div>
</template>

<script>
export default {
  name: 'LandingPage'
}
</script>

<style scoped>
#banner {
    background-image: url("~@/assets/landing_banner.webp");
    background-repeat: no-repeat;
    background-position: center;
    background-size:cover;
    height: 300px;
    margin-bottom: 20px;
}
#banner h3{
    color: white;
    text-shadow: 2px 2px #111111;
}
</style>
