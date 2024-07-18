<template>
    <v-card class="container" elevation="4">
        <v-card-title class="card-title">User Settings</v-card-title>
        <v-card-item>
            <v-form>
                <v-text-field
                    v-model="username"
                    color="primary"
                    label="Username"
                    variant="underlined"
                    :rules="[() => !!username || 'This field is required']"
                    required
                ></v-text-field>

                <v-text-field
                    v-model="password"
                    color="primary"
                    label="Password"
                    placeholder="Enter your password"
                    variant="underlined"
                    required
                    :rules="[() => !!password || 'This field is required']"
                    type="password"
                    autocomplete="on"
                ></v-text-field>

                <v-text-field
                    v-model="password2"
                    color="primary"
                    label="Re-Enter Password"
                    placeholder="Re-Enter your password"
                    :rules="[() => password === password2 || 'Password must match']"
                    variant="underlined"
                    required
                    type="password"
                    autocomplete="on"
                ></v-text-field>

                <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn @click="registerHandler">
                    Update User Information

                    <v-icon icon="mdi-chevron-right" end></v-icon>
                </v-btn>
                </v-card-actions>
            </v-form>
        </v-card-item>
    </v-card>
    <v-snackbar
        v-if="text"
        v-model="snackBar"
        :timeout="timeout"
    >
        {{ text }}

      <template v-slot:actions>
        <v-btn
          color="blue"
          variant="text"
          @click="snackBar = false"
        >
          Close
        </v-btn>
      </template>
    </v-snackbar>
</template>

<script>
import { mapActions, mapState } from 'vuex';

export default { 
    emits: ['signed-in'],
    data() {
        return {
            username: '',
            userType: null,
            userTypeDisplay: null,
            password: '',
            password2: '',
            timeout: 3000,
            text: '',
            snackBar: false,
        };
    },

    computed: {
        ...mapState(['user']),
    },

    methods: {
        ...mapActions(['updateUserInformation', 'fetchSpecificUser']),

        async registerHandler() {
            this.userType = this.userTypeDisplay === 'administrator' ? 1 : 2;
            let payload = {
                id: this.user.admin.id,
                username: this.username,
            };

            if (this.password) {
                payload['password'] = this.password;
            }

            let response = await this.updateUserInformation(payload);
            if (response === 200) {
                this.text = 'User Login Information Updated';
                this.snackBar = true;
            } else {
                this.text = 'Invalid Inputs'
            }
            
        }
    },

    async created() {
        let user_id = localStorage.getItem('user_id');
        await this.fetchSpecificUser(user_id);

        this.username = this.user.admin.username;
        this.userTypeDisplay = this.user.user_type_display;
    }
}
</script>

<style scoped>
    .card-title {
        margin: 8px 0px 8px 0px;
        font-size: 40px;
    }
</style>
