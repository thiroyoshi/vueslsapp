<template>
    <v-container id="home-content">
        <!-- GET -->
        <v-card raised>
            <v-list-item>
                <v-list-item-content>
                    <v-list-item-title>GET REST API Request</v-list-item-title>
                    <v-list-item-subtitle>Test REST API</v-list-item-subtitle>
                </v-list-item-content>
            </v-list-item>
            <v-divider />
            <v-form class="input-form">
                <v-btn 
                    @click="getMessage"
                    color="primary"
                    :disabled="getAPILoading"
                >GET Message</v-btn>
                <v-progress-circular
                    v-show="getAPILoading"
                    class="api-loading"
                    indeterminate
                    size=20
                    width=3
                    color="primary"
                ></v-progress-circular>
                <v-textarea
                    class="api-result"
                    outlined
                    counter
                    no-resize
                    readonly
                    label="API Result"
                    v-model="getApiResult"
                ></v-textarea>
            </v-form>
        </v-card>
        <br />

        <!-- POST -->
        <v-card raised>
            <v-list-item>
                <v-list-item-content>
                    <v-list-item-title>POST REST API Request</v-list-item-title>
                    <v-list-item-subtitle>Test REST API</v-list-item-subtitle>
                </v-list-item-content>
            </v-list-item>
            <v-divider />
            <v-form class="input-form">
                <v-text-field
                    counter
                    v-model="postApiBody.message"
                    label="Message"
                ></v-text-field>
                <v-btn 
                    @click="postMessage"
                    color="primary"
                    :disabled="postAPILoading"
                    >POST Message</v-btn>
                <v-progress-circular
                    v-show="postAPILoading"
                    class="api-loading"
                    indeterminate
                    size=20
                    width=3
                    color="primary"
                ></v-progress-circular>
                <v-textarea
                    class="api-result"
                    outlined
                    counter
                    no-resize
                    readonly
                    label="API Result"
                    v-model="postApiResult"
                ></v-textarea>
            </v-form>
        </v-card>
        <br />

        <!-- PUT -->
        <v-card raised>
            <v-list-item>
                <v-list-item-content>
                    <v-list-item-title>PUT REST API Request</v-list-item-title>
                    <v-list-item-subtitle>Test REST API</v-list-item-subtitle>
                </v-list-item-content>
            </v-list-item>
            <v-divider />
            <v-form class="input-form">
                <v-text-field
                    counter
                    v-model="putApiBody.message"
                    label="Message"
                ></v-text-field>
                <v-text-field
                    counter
                    v-model="putApiBody.message_id"
                    label="Message ID"
                ></v-text-field>
                <v-btn 
                    @click="putMessage" 
                    color="primary"
                    :disabled="putAPILoading"
                    >PUT Message</v-btn>
                <v-progress-circular
                    v-show="putAPILoading"
                    class="api-loading"
                    indeterminate
                    size=20
                    width=3
                    color="primary"
                ></v-progress-circular>
                <v-textarea
                    class="api-result"
                    outlined
                    counter
                    no-resize
                    readonly
                    label="API Result"
                    v-model="putApiResult"
                ></v-textarea>
            </v-form>
        </v-card>
        <br />

        <!-- DELETE -->
        <v-card raised>
            <v-list-item>
                <v-list-item-content>
                    <v-list-item-title>DELETE REST API Request</v-list-item-title>
                    <v-list-item-subtitle>Test REST API</v-list-item-subtitle>
                </v-list-item-content>
            </v-list-item>
            <v-divider />
            <v-form class="input-form">
                <v-text-field
                    counter
                    v-model="deleteApiBody.message_id"
                    label="Message ID"
                ></v-text-field>
                <v-btn 
                    @click="deleteMessage" 
                    color="primary"
                    :disabled="deleteAPILoading"
                    >DELETE Message</v-btn>
                <v-progress-circular
                    v-show="deleteAPILoading"
                    class="api-loading"
                    indeterminate
                    size=20
                    width=3
                    color="primary"
                ></v-progress-circular>
                <v-textarea
                    class="api-result"
                    outlined
                    counter
                    no-resize
                    readonly
                    label="API Result"
                    v-model="deleteApiResult"
                ></v-textarea>
            </v-form>
        </v-card>

        <v-dialog v-model="dialog" persistent max-width="500">
        <v-card>
            <v-card-title>API Request Failed</v-card-title>
            <v-card-text>{{ errorMessage }}</v-card-text>
            <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="green darken-1" text @click="dialog = false">OK</v-btn>
            </v-card-actions>
        </v-card>
        </v-dialog>
        
    </v-container>
</template>

<script>
export default {
    name: 'home',
    data: function() {
        return {
            apiHeaders: {
                'Authorization': localStorage.idToken,
                'Content-Type': 'application/json',
            },
            getApiResult: "",
            getAPILoading: false,
            postApiResult: "",
            postAPILoading: false,
            putApiResult: "",
            putAPILoading: false,
            deleteApiResult: "",
            deleteAPILoading: false,
            postApiBody: {
                message: "",
            },
            putApiBody: {
                message_id: "",
                message: "",
            },
            deleteApiBody: {
                message_id: "",
            },
            errorMessage: "",
            dialog: false
        }
    },
    methods: {
        getMessage: function(){
            this.getApiResult = ""
            var url = process.env.VUE_APP_API_ORIGIN + "/messages"
            var config = {
                headers: this.apiHeaders,
                responseType: 'json'
            };
            this.getAPILoading = true
            this.axios.get(url, config)
            .then(res => {
                this.getAPILoading = false
                this.getApiResult = JSON.stringify(res.data.messages, null , "\t");
            })
            .catch(err => {
                this.getAPILoading = false
                this.errorMessage = err.message
                this.dialog = true
            })
        },
        postMessage: function(){
            this.postApiResult = ""
            var url = process.env.VUE_APP_API_ORIGIN + "/messages"
            var config = {
                headers: this.apiHeaders,
                responseType: 'json'
            };
            this.postAPILoading = true
            this.axios.post(url, this.postApiBody, config)
            .then(res => {
                this.postAPILoading = false
                this.postApiResult = JSON.stringify(res.data.message, null , "\t");
            })
            .catch(err => {
                this.postAPILoading = false
                this.errorMessage = err.response.data.message
                this.dialog = true
            })
        },
        putMessage: function(){
            this.putApiResult = ""
            var url = process.env.VUE_APP_API_ORIGIN + "/messages"
            var config = {
                headers: this.apiHeaders,
                responseType: 'json'
            };
            this.putAPILoading = true
            this.axios.put(url, this.putApiBody, config)
            .then(res => {
                this.putAPILoading = false
                this.putApiResult = JSON.stringify(res.data.message, null , "\t");
            })
            .catch(err => {
                this.putAPILoading = false
                this.errorMessage = err.response.data.message
                this.dialog = true
            })
        },
        deleteMessage: function(){
            this.deleteApiResult = ""
            var url = process.env.VUE_APP_API_ORIGIN + "/messages"
            var config = {
                headers: this.apiHeaders,
                data: this.deleteApiBody,
                responseType: 'json'
            };
            this.deleteAPILoading = true
            this.axios.delete(url, config)
            .then(res => {
                this.deleteAPILoading = false
                this.deleteApiResult = JSON.stringify(res.data.message, null , "\t");
            })
            .catch(err => {
                this.deleteAPILoading = false
                this.errorMessage = err.response.data.message
                this.dialog = true
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