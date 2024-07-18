<template>
    <v-card class="container" elevation="4">
        <v-card-title class="card-title">Courses</v-card-title>
        <v-fade-transition>
            <v-alert v-if="alertTitle" :title="alertTitle" :type="alertType" :text="alertText" variant="outlined"></v-alert>
        </v-fade-transition>
        <v-card-item v-if="userType==='administrator'">
            <v-btn variant="outlined" size="small" @click="addCourse">
            Add Course
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
                    Name
                </th>
                <th class="text-left">
                    Group Number
                </th>
                <th class="text-left">
                </th>
                <th class="text-left">
                </th>
                </tr>
            </thead>
            <tbody>
                <tr
                v-for="course in computedCourses"
                :key="course.id"
                >
                <td>{{ course.course_code }}</td>
                <td>{{ course.name ? course.name : 'No Name' }}</td>
                <td>{{ course.group_number }}</td>
                <td v-if="userType==='administrator'">
                    <v-btn variant="outlined" size="small" @click="openEditCourse(course)">
                        Edit
                    </v-btn>
                </td>
                <td v-else></td>
                <td v-if="userType==='administrator'">
                    <v-btn variant="outlined" size="small" @click="deleteselectedCourse(course)">
                        Delete Course
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
            <createEditCourse
                :course="selectedCourse"
                @close="dialog=false"
                @add-course="createNewCourse"
                @save-changes="editCourse"/>
        </v-dialog>
    </v-card>
  </template>

<script>
import createEditCourse from '@/components/createEditCourse.vue'
import { mapActions, mapState} from 'vuex';
export default {
  name: 'courses',
  components: {
    createEditCourse,
  },
  data () {
    return {
      dialog: false,
      selectedCourse: {},
      alertTitle: '',
      alertText: '',
      alertType: '',
      timeout: 3000,
      userType: ''
    }
  },

  computed: {
    ...mapState(['courses']),

    computedCourses() {
        return this.courses;
    }
  },
  

  methods: {
    ...mapActions(['fetchCourses', 'createCourse', 'deleteCourse', 'updateCourse']),

    openEditCourse(course) {
        this.selectedCourse = course;
        this.dialog = true;
    },

    addCourse() {
        this.selectedCourse = {};
        this.dialog = true;
    },

    async createNewCourse(newCourse) {
        await this.createCourse(newCourse);
        this.dialog = false;
    },

    async deleteselectedCourse(course) {
        if (course.has_schedule) {
            this.alertTitle = 'Unable to Delete Course';
            this.alertText = 'There are existing Schedules with this Course';
            this.alertType = 'error';
            setTimeout(() => {
                    this.alertTitle = '';
                    this.alertText = '';
                    this.alertType = '';
                }, 3000);
        } else {
            await this.deleteCourse(course.id);
        }
    },

    async editCourse(editedCourse) {
        await this.updateCourse(editedCourse);
        this.dialog = false;
    }
  },

  async created() {
    await this.fetchCourses();
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
