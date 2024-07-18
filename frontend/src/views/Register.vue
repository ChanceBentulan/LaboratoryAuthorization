<template>
    <v-card class="container" elevation="4">
        <v-card-title class="card-title">Register Account</v-card-title>
        <v-card-item>
            <v-form>
                <v-text-field
                    v-model="first"
                    color="primary"
                    label="First name"
                    variant="underlined"
                    :rules="[() => !!first || 'This field is required']"
                    required
                ></v-text-field>

                <v-text-field
                    v-model="last"
                    color="primary"
                    label="Last name"
                    variant="underlined"
                    :rules="[() => !!last || 'This field is required']"
                    required
                ></v-text-field>

                <v-text-field
                    v-model="idNumber"
                    color="primary"
                    label="ID Number"
                    variant="underlined"
                    :rules="[() => !!idNumber || 'This field is required']"
                    required
                ></v-text-field>

                <v-text-field
                    v-model="serial"
                    color="primary"
                    label="RFID Number"
                    variant="underlined"
                    :rules="[() => !!serial || 'This field is required']"
                    required
                ></v-text-field>

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

                <v-select
                    v-model="userTypeDisplay"
                    label="User Type"
                    :items="['administrator', 'staff']"
                    :rules="[() => !!userTypeDisplay || 'This field is required']"
                    variant="underlined"
                ></v-select>

                <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn @click="registerHandler">
                    Complete Registration

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
import { mapActions } from 'vuex';

export default { 
    emits: ['signed-in'],
    data() {
        return {
            first: '',
            last: '',
            idNumber: '',
            serial: '',
            username: '',
            password: '',
            password2: '',
            userType: null,
            userTypeDisplay: null,
            timeout: 3000,
            text: '',
            snackBar: false,
        };
    },

    methods: {
        ...mapActions(['registerUser']),

        async registerHandler() {
            this.userType = this.userTypeDisplay === 'administrator' ? 1 : 2;
            let payload = {
                first_name: this.first,
                last_name: this.last,
                id_number: this.idNumber,
                username: this.username,
                password: this.password,
                user_type: this.userType,
                serial: this.serial
            };

            let response = await this.registerUser(payload);
            if (response.status === 201) {
                this.text = response.data.message;
                this.snackBar = true;
                this.first = '';
                this.last = '';
                this.idNumber = '';
                this.username = '';
                this.password = '';
                this.password2 = '';
                this.serial = '';
                this.userType = null;
                this.userTypeDisplay = null;
            } else {
                this.text = 'Invalid Inputs'
            }
            
        }
    }
}
</script>

<style scoped>
    .card-title {
        margin: 8px 0px 8px 0px;
        font-size: 40px;
    }
</style>
