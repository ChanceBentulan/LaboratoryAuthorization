<template>
    <v-card class="container" elevation="4">
        <v-card-title class="card-title">Schedules For {{ schedulesToday?.full_date_today }}</v-card-title>
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
                </tr>
            </thead>
            <tbody>
                <tr
                  v-for="schedule in schedulesToday?.course_schedules"
                  :key="schedule.id"
                >
                <td>{{ schedule.course }}</td>
                <td>{{ schedule.days}}</td>
                <td>{{ schedule.start_time }}</td>
                <td>{{ schedule.end_time }}</td>
                <td>{{ schedule.room }}</td>
                </tr>
            </tbody>
        </v-table>
        </v-card-item>
    </v-card>
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
            text: ''
        }
    },

    computed: {
        ...mapState(['courseSchedules', 'courses', 'masterList', 'usersInSchedule', 'schedulesToday']),

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
            this.fetchScheduleToday()
        ]);
    },

    methods: {
        ...mapActions(
            ['fetchScheduleToday']),
    }
  }
</script>

<style scoped>
    .card-title {
        margin: 8px 0px 8px 0px;
        font-size: 40px;
    }
</style>
