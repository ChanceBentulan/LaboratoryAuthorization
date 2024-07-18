<template>
    <v-card class="card">
        <v-card-text v-if="!Object.keys(user).length">
          Create User
        </v-card-text>
        <v-card-text v-else>
          Edit User
        </v-card-text>
        <v-container>
            <v-row>
              <v-col
                cols="12"
                sm="6"
                md="4"
              >
                <v-text-field
                  label="ID Number*"
                  required
                  v-model="specificUser.id_number"
                  :rules="[rules.counter]"
                ></v-text-field>
              </v-col>
              <v-col
                cols="12"
                sm="6"
                md="4"
              >
                <v-text-field
                  label="Serial ID*"
                  required
                  v-model="specificUser.serial"
                ></v-text-field>
              </v-col>
              <v-col
                cols="12"
                sm="6"
                md="4"
              >
                <v-text-field
                  label="First Name*"
                  required
                  v-model="specificUser.first_name"
                ></v-text-field>
              </v-col>
              <v-col
                cols="12"
                sm="6"
                md="4"
              >
                <v-text-field
                  label="Last Name*"
                  required
                  v-model="specificUser.last_name"
                ></v-text-field>
              </v-col>
              <v-col
                cols="12"
                sm="6"
              >
                <v-select
                  :items="['student', 'faculty']"
                  label="User Type*"
                  required
                  v-model="specificUser.user_type_display"
                ></v-select>
              </v-col>
            </v-row>
          </v-container>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
                color="blue-darken-1"
                variant="text"
                @click="$emit('close')"
            >
                Close
            </v-btn>
            <v-btn
                v-if="!Object.keys(user).length"
                color="blue-darken-1"
                variant="text"
                @click="$emit('add-user', specificUser)"
            >
                Add User
            </v-btn>
            <v-btn
                v-else
                color="blue-darken-1"
                variant="text"
                @click="$emit('save-changes', specificUser)"
            >
                Save Changes
            </v-btn>
        </v-card-actions>
    </v-card>
</template>

<script>
export default{ 
    name: 'CreateEditUser',
    props: {
        dialog: {
            type: Boolean,
            required: false,
        },

        user: {
          type: Object,
          required: true
        }
    },

    data() {
      return {
        specificUser: {
          id: this.user?.id ? this.user?.id : null,
          serial: this.user?.serial ? this.user.serial : null,
          id_number: this.user?.id_number ? this.user.id_number : null,
          first_name: this.user?.first_name ? this.user.first_name : '',
          last_name: this.user?.last_name ? this.user.last_name : '',
          user_type_display: this.user?.user_type_display ? this.user.user_type_display : '',
          user_type: this.user?.user_type ? this.user.user_type : null,
        },
        rules: {
          counter: value => value?.length <= 8 || `Max 8 characters`
        }
      };
    }
}
</script>

<style scoped>
.card {
    width: 800px;
}
</style>
