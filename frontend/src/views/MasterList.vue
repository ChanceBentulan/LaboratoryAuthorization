<template>
    <v-card class="container" elevation="4">
        <v-card-title class="card-title">MasterList</v-card-title>
        <v-fade-transition>
            <v-alert v-if="alertTitle" :title="alertTitle" :type="alertType" :text="alertText" variant="outlined"></v-alert>
        </v-fade-transition>
        <v-card-item v-if="userType==='administrator'">
            <v-btn variant="outlined" size="small" @click="addUser">
            Add User
            </v-btn>
        </v-card-item>
        <v-card-item>
            <v-table fixed-header>
            <thead>
                <tr>
                <th class="text-left">
                    ID Number
                </th>
                <th class="text-left">
                    Name
                </th>
                <th class="text-left">
                    User Type
                </th>
                <th class="text-left">
                </th>
                <th class="text-left">
                </th>
                </tr>
            </thead>
            <tbody>
                <tr
                v-for="user in users"
                :key="user.id_number"
                >
                <td>{{ user.id_number }}</td>
                <td>{{ user.full_name}}</td>
                <td>{{ user.user_type_display }}</td>
                <td v-if="userType==='administrator'">
                    <v-btn variant="outlined" size="small" @click="openEditUser(user)">
                        Edit
                    </v-btn>
                </td>
                <td v-else></td>
                <td v-if="userType==='administrator'">
                    <v-btn variant="outlined" size="small" @click="deleteSelectedUser(user)">
                        Delete User
                    </v-btn>
                </td>
                <td v-else></td>
                </tr>
            </tbody>
        </v-table>
        </v-card-item>
        <v-dialog
            v-if="dialog"
            activator="parent"
            width="auto"
        >
            <CreateEditUser
                :user="selectedUser"
                @close="dialog=false"
                @add-user="createNewUser"
                @save-changes="editUser"/>
        </v-dialog>
    </v-card>
  </template>

<script>
    import CreateEditUser from '@/components/CreateEditUser.vue'
    import { mapActions, mapState} from 'vuex';

    export default {
        name: 'MasterList',
        components: {
            CreateEditUser,
        },
        data () {
            return {
            dialog: false,
            selectedUser: null,
            alertTitle: '',
            alertText: '',
            alertType: '',
            userType: '',
            }
        },

        computed: {
            ...mapState(['masterList']),

            users() {
                return this.masterList;
            }
        },
        
        methods: {
            ...mapActions(['fetchMasterList', 'createUser', 'deleteUser', 'updateUser']),

            openEditUser(user) {
                this.selectedUser = user;
                this.dialog = true;
            },

            addUser() {
                this.selectedUser = {};
                this.dialog = true;
            },

            async createNewUser(newUser) {
                if (newUser.user_type_display === 'student') {
                    newUser.user_type = 0;
                } else if (newUser.user_type_display === 'administrator') {
                    newUser.user_type = 1;
                } else if (newUser.user_type_display === 'staff') {
                    newUser.user_type = 2;
                } else {
                    newUser.user_type = 3;
                }

                await this.createUser(newUser);

                this.dialog = false;
            },

            async deleteSelectedUser(user) {
                if (user.has_schedule) {
                    this.alertTitle = 'Unable to delete User';
                    this.alertText = 'User belongs to a specific schedule';
                    this.alertType = 'error';
                    setTimeout(() => {
                            this.alertTitle = '';
                            this.alertText = '';
                            this.alertType = '';
                        }, 3000);
                } else {
                    await this.deleteUser(user.id);
                }
            },

            async editUser(editedUser) {
                if (editedUser.user_type_display === 'student') {
                    editedUser.user_type = 0;
                } else if (editedUser.user_type_display === 'administrator') {
                    editedUser.user_type = 1;
                } else if (editedUser.user_type_display === 'staff') {
                    editedUser.user_type = 2;
                } else {
                    editedUser.user_type = 3;
                }
                await this.updateUser(editedUser);

                this.dialog = false;
            }
        },

        async created() {
            await this.fetchMasterList();
            this.userType = localStorage.getItem('user_type');
        }
    }
</script>



<style scoped>
.card-title {
    margin: 8px 0px 8px 0px;
    font-size: 40px;
}
</style>
