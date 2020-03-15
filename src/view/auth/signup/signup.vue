<template>
    <div id="signup-content">
        <v-layout justify-center>
            <Signup />
        </v-layout>
        <v-alert type="error" id="signup-alert">
            Do NOT use the serious password you usually use, because this is a sample app and do not use HTTPS.
        </v-alert>        
        <v-layout justify-center>
            <router-link to="/">
                <v-btn text small id="back-btn">
                    <v-icon id="back-icon">fa-arrow-left</v-icon>back to home
                </v-btn>
            </router-link>
        </v-layout>
    </div>
</template>

<script>
import Signup from "../../../components/auth/signup";

export default {
    name: 'SignupView',
    components: {
        Signup,
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
#signup-content {
    margin-top: 25px;
}
#signup-alert {
    margin-top: 20px;
    margin-right: 20%;
    margin-left: 20%;
}
</style>
