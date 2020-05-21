<template>
  <v-app-bar
    app
    color="rgba（255、0、0、0.5）"
    dark
  >
    <v-toolbar-title
      id="title"
      @click="clickTitle"
    >
      {{ title }}
    </v-toolbar-title>

    <v-spacer />

    <template v-if="this.$store.getters.isAuth">
      <v-menu offset-y>
        <template v-slot:activator="{ on }">
          <v-btn
            target="_blank"
            text
            v-on="on"
          >
            <v-icon>mdi-menu</v-icon>
          </v-btn>
        </template>
        <v-list>
          <v-list-item @click="goToSettings">
            <v-icon :style="{marginRight: '10px'}">
              fa-user-cog
            </v-icon>
            <span>{{ $t("header.settings") }}</span>
          </v-list-item>
          <v-list-item @click="logout">
            <v-icon :style="{marginRight: '10px'}">
              fa-sign-out-alt
            </v-icon>
            <span>{{ $t("header.logout") }}</span>
          </v-list-item>
        </v-list>
      </v-menu>
    </template>
  </v-app-bar>
</template>

<script>
export default {
  name: 'GlobalHeader',
  props: {
    title: {
      type: String,
      required: true
    }
  },
  methods: {
    clickTitle: function () {
      if (this.$route.path === '/') { return }

      if (this.$store.getters.isAuth) {
        this.$router.replace('/home')
      } else {
        this.$router.replace('/')
      }
    },
    goToSettings: function () {
      this.$router.replace('/settings')
    },
    logout: function () {
      this.$cognito.logout()
      localStorage.clear()
      this.$store.commit('setIsAuth')
      this.$router.replace('/login')
    }
  }
}
</script>

<style scoped>
v-icon {
  margin: 10px;
}
#title {
  text-decoration: none;
  color: white;
  cursor: hand;
  cursor:pointer;
}
</style>
