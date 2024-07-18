<template>
    <v-card class="container" elevation="4">
        <v-card-title class="card-title">Schedules</v-card-title>
        <v-fade-transition>
            <v-alert v-if="alertTitle" :title="alertTitle" :type="alertType" :text="alertText" variant="outlined"></v-alert>
        </v-fade-transition>
        <v-card-item v-if="userType==='administrator'">
            <v-btn variant="outlined" size="small" class="mr-4" @click="addCourseSchedule">
                Add Schedule
            </v-btn>
            <v-btn variant="outlined" size="small" @click="openCSV=true">
                Upload CSV
            </v-btn>
        </v-card-item>
        <v-card-item>
            <v-table fixed-header>
            <thead>
                <tr>
                <th class="text-left">
                    Course Code
                </th>
                <th class="text-left">
                    Days
                </th>
                <th class="text-left">
                    Start Time
                </th>
                <th class="text-left">
                    End Time
                </th>
                <th class="text-left">
                    Room
                </th>
                <th class="text-left">
                </th>
                <th class="text-left">
                </th>
                <th class="text-left">
                </th>
                </tr>
            </thead>
            <tbody>
                <tr
                  v-for="schedule in computedCourseSchedules"
                  :key="schedule.id"
                >
                <td>{{ schedule.course.course_code }}</td>
                <td>{{ schedule.days}}</td>
                <td>{{ schedule.start_time }}</td>
                <td>{{ schedule.end_time }}</td>
                <td>{{ schedule.room }}</td>
                <td v-if="userType==='administrator'">
                    <v-btn variant="outlined" size="small" @click="openEditCourseSchedule(schedule)">
                        Edit
                    </v-btn>
                </td>
                <td v-else></td>
                <td v-if="userType==='administrator'">
                    <v-btn variant="outlined" size="small" @click="openAddUser(schedule.id)">
                        Add Users
                    </v-btn>
                </td>
                <td v-else></td>
                <td v-if="userType==='administrator'">
                    <v-btn variant="outlined" size="small" @click="deleteSelectedCourseSchedule(schedule)">
                        Delete Schedules
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
            <CreateEditSchedule
                :course-schedule="selectedCourseSchedule"
                @close="dialog=false"
                @add-course-schedule="createNewCourseSchedule"
                @save-changes="editCourseSchedule"/>
        </v-dialog>
        <base-modal v-if="showModal" :size="'medium'">
            <template v-slot:header>
                <div class="modal-header">
                    <h5>Add Users to Schedule</h5>
                </div>
            </template>

            <template v-slot:body>
                <div class="modal-body">
                    <v-tabs
                        v-model="tab"
                        bg-color="primary"
                    >
                        <v-tab value="one">Users in schedule</v-tab>
                        <v-tab value="two">All Users</v-tab>
                    </v-tabs>
                    <v-window v-model="tab">
                        <v-window-item value="one">
                            <v-item-group v-model="userIdsOne" multiple>
                                <v-container>
                                    <v-row>
                                        <v-col
                                        v-for="user in usersInsideSchedule.users_in_schedule"
                                        :key="user.id"
                                        cols="16"
                                        md="4"
                                        >
                                        <v-item v-slot="{ isSelected, toggle }">
                                            <v-card
                                            :color="isSelected ? 'primary' : ''"
                                            class="d-flex align-center"
                                            height="100"
                                            dark
                                            @click="toggle"
                                            >
                                            <v-scroll-y-transition>
                                                <div
                                                class="flex-grow-1 text-center"
                                                >
                                                    {{ user.full_name }}
                                                </div>
                                            </v-scroll-y-transition>
                                            </v-card>
                                        </v-item>
                                        </v-col>
                                    </v-row>
                                </v-container>
                            </v-item-group>
                        </v-window-item>
                        <v-window-item value="two">
                            <v-item-group v-model="userIdsTwo" multiple>
                                <v-container>
                                    <v-row>
                                        <v-col
                                        v-for="user in usersInsideSchedule.user_not_in_schedule"
                                        :key="user.id"
                                        cols="16"
                                        md="4"
                                        >
                                        <v-item v-slot="{ isSelected, toggle }">
                                            <v-card
                                            :color="isSelected ? 'primary' : ''"
                                            class="d-flex align-center"
                                            height="100"
                                            dark
                                            @click="toggle"
                                            >
                                            <v-scroll-y-transition>
                                                <div
                                                class="flex-grow-1 text-center"
                                                >
                                                    {{ user.full_name }}
                                                </div>
                                            </v-scroll-y-transition>
                                            </v-card>
                                        </v-item>
                                        </v-col>
                                    </v-row>
                                </v-container>
                            </v-item-group>
                        </v-window-item>
                    </v-window>
                </div>
            </template>

            <template v-slot:footer>
                <div class="modal-body">
                    <v-btn variant="outlined" size="small" @click="showModal=false">
                        Close
                    </v-btn>

                    <v-btn variant="outlined" size="small" @click="peoplePickerHandler(selectedCourseSchedulePk)" >
                        Save Changes
                    </v-btn>
                </div>
            </template>
        </base-modal>
    </v-card>
    <v-dialog
        v-if="openCSV"
        activator="parent"
        width="auto"
    >
        <UploadCSV
            @done-upload="handleSnackBar"/>
    </v-dialog>
    <v-snackbar
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
  import CreateEditSchedule from '@/components/CreateEditSchedule.vue'
  import BaseModal from '@/components/generics/BaseModal.vue'
  import UploadCSV from '@/components/UploadCSV.vue'
  import { mapActions, mapState} from 'vuex';

  export default {
    name: 'Schedules',
    emits: ['signed-in'],
    components: {
        CreateEditSchedule,
        BaseModal, 
        UploadCSV
    },

    data () {
        return {
            dialog: false,
            selectedCourseSchedule: {},
            showModal: false,
            userIdsOne: [],
            userIdsTwo: [],
            tab: null,
            selectedCourseSchedulePk: null ,
            openCSV: false,
            alertTitle: '',
            alertText: '',
            alertType: '',
            snackBar: false,
            timeout: 3000,
            text: '',
            userType: ''
        }
    },

    computed: {
        ...mapState(['courseSchedules', 'courses', 'masterList', 'usersInSchedule']),

        computedCourseSchedules() {
            return this.courseSchedules;
        },

        users() {
            return this.masterList;
        },

        usersInsideSchedule() {
            return this.usersInSchedule;
        }
    },

    async created() {
        await Promise.all([
            this.fetchCourses(),
            this.fetchCourseSchedules()
        ]);
        this.userType = localStorage.getItem('user_type');
    },

    methods: {
        ...mapActions(
            ['fetchCourses', 'fetchCourseSchedules', 'createCourseSchedule',
            'deleteCourseSchedule', 'updateCourseSchedule', 'addUsersToSchedule',
            'fetchUsersInSchedule', 'fetchSpecificCourseSchedule']),

        async handleSnackBar(text) {
            await this.fetchCourseSchedules();
            this.openCSV = false;
            this.text = text;
            this.snackBar = true;
        },

        openEditCourseSchedule(courseSchedule) {
          this.selectedCourseSchedule = courseSchedule;
          this.dialog = true;
        },

        addCourseSchedule() {
            this.selectedCourseSchedule = {};
            this.dialog = true;
        },

        async createNewCourseSchedule(newCourseSchedule) {
            let course = this.courses.find(
                course => course.course_code === newCourseSchedule.course_code);
            newCourseSchedule['course_id'] = course.id;
            newCourseSchedule['start_time'] = JSON.stringify(newCourseSchedule.start_time)
            newCourseSchedule['end_time'] = JSON.stringify(newCourseSchedule.end_time)

            await this.createCourseSchedule(newCourseSchedule);
            this.dialog = false;
        },

        async deleteSelectedCourseSchedule(schedule) {
            if (schedule.user_pks.length === 0){
                await this.deleteCourseSchedule(schedule.id);
            } else {
                this.alertTitle = 'Unable to delete schedule';
                this.alertText = 'There are users belonging inside the schedule';
                this.alertType = 'error';
                setTimeout(() => {
                        this.alertTitle = '';
                        this.alertText = '';
                        this.alertType = '';
                    }, 3000);
            }
        },

        async editCourseSchedule(editedCourseSchedule) {
            await this.updateCourseSchedule(editedCourseSchedule);
            this.dialog = false;
        },

        async openAddUser(sched_id) {
            await this.fetchUsersInSchedule(sched_id);
            this.userIdsTwo = []
            this.userIdsOne = []
            let users_in_schedule_len = this.usersInsideSchedule.users_in_schedule.length;
            this.userIdsOne = Array.from({length: users_in_schedule_len}, (_, index) => index);
            this.selectedCourseSchedulePk=sched_id;
            this.showModal = true;
        },

        async peoplePickerHandler(course_schedule_id) {
           let user_ids_one = this.userIdsOne.map(index => this.usersInsideSchedule.users_in_schedule[index].id)
           let user_ids_two = this.userIdsTwo.map(index => this.usersInsideSchedule.user_not_in_schedule[index].id);
           let user_ids = user_ids_one.concat(user_ids_two)
           let payload = {
            'user_ids': user_ids,
            'course_schedule_id': course_schedule_id
           }
           await this.addUsersToSchedule(payload);
           await this.fetchSpecificCourseSchedule(course_schedule_id);
           this.showModal = false
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
