<template>
    <div id="content">
        <v-container fluid id="banner">
            <v-layout justify-center>
                <h3>This is Vue + Serverless Framework App</h3>
            </v-layout>
        </v-container>
        <v-container>
            <v-row class="mb-6" justify="center" no-gutters>
                <div class="pa-3">
                    <v-btn class="pa-3" color="primary" href="/login">Login</v-btn>
                </div>
                <div class="pa-3">
                  <v-btn color="primary" href="/agreement">Signup</v-btn>
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
