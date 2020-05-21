<template>
  <div id="notfound-content">
    <v-layout justify-center>
      <h1 id="status-code">
        404
      </h1>
    </v-layout>
    <v-layout justify-center>
      <h2>{{ $t("notfound.title") }}</h2>
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
          </v-icon>{{ $t("notfound.toHome") }}
        </v-btn>
      </router-link>
    </v-layout>
  </div>
</template>

<script>
export default {
  name: 'NotFound'
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
#notfound-content {
    margin-top: 70px;
}
#status-code {
    font-size: 72px;
}
</style>
