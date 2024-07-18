<template>
    <v-card class="card overflow-visible">
        <v-card-text v-if="!Object.keys(courseSchedule).length">
          Create Schedule
        </v-card-text>
        <v-card-text v-else>
          Edit Schedule
        </v-card-text>
        <v-container>
            <v-row>
              <VueDatePicker 
                v-model="time" 
                time-picker
                :range="{ disableTimeRangeValidation: true }"
                placeholder="Start Time - End Time"
              />
              <v-col
                cols="12"
                sm="6"
                md="4"
              >
                <v-select
                  :items="courseCodeList"
                  label="Course Code"
                  required
                  v-model="specificSchedule.course_code"
                ></v-select>
              </v-col>
              <v-col
                cols="12"
                sm="6"
                md="4"
              >
              <v-select
                v-model="selectedDays"
                :items="days"
                label="Days"
                multiple
              ></v-select>
              </v-col>
              <v-col
                cols="12"
                sm="6"
                md="4"
              >
                <v-text-field
                  label="Room"
                  required
                  v-model="specificSchedule.room"
                ></v-text-field>
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
                v-if="!Object.keys(courseSchedule).length"
                color="blue-darken-1"
                variant="text"
                @click="$emit('add-course-schedule', specificSchedule)"
            >
                Add Course Schedule
            </v-btn>
            <v-btn
                v-else
                color="blue-darken-1"
                variant="text"
                @click="validateEdit"
            >
                Save Changes
            </v-btn>
        </v-card-actions>
    </v-card>
</template>

<script>
  import { mapState } from 'vuex';
  import VueDatePicker from '@vuepic/vue-datepicker';
  import '@vuepic/vue-datepicker/dist/main.css';

  export default{
      name: 'CreateEditSchedule',

      components: {
        VueDatePicker
      },

      props: {
          dialog: {
            type: Boolean,
            required: false,
          },

          courseSchedule: {
            type: Object,
            required: true,
          }
      },

      data() {
          return {
              specificSchedule: {
                id: this.courseSchedule?.id ? this.courseSchedule?.id : null,
                course_code: this.courseSchedule?.course?.course_code ? this.courseSchedule?.course?.course_code : null,
                days: this.courseSchedule?.days ? this.courseSchedule?.days : null,
                start_time: this.courseSchedule?.start_time ? this.courseSchedule?.start_time : null,
                end_time: this.courseSchedule?.end_time ? this.courseSchedule?.end_time : null,
                room: this.courseSchedule?.room ? this.courseSchedule?.room: null,
              },
              time: [],
              days: ['Monday', 'Tuesday', 'Wednesday','Thursday', 'Friday', 'Saturday', 'Sunday'],
              selectedDays: []
          };
      },

      computed: {
          ...mapState(['courses']),

          courseCodeList() {
            return this.courses.map(course => course.course_code);
          }
      },

      watch: {
          time: {
              handler(value) {
                let startTime = [value[0].hours, value[0].minutes];
                let endTime = [value[1].hours, value[1].minutes];

                this.specificSchedule.start_time = startTime;
                this.specificSchedule.end_time = endTime;
              }
          },

          selectedDays: {
            handler(value) {
              this.specificSchedule.days = value.map(day => day.toLowerCase().substring(0,2)).join('|');
            }
          }
      },

      methods: {
        
        validateEdit() {
          let startTime = [parseInt(this.time[0].hours), parseInt(this.time[0].minutes)];
          let endTime = [parseInt(this.time[1].hours), parseInt(this.time[1].minutes)];
          this.specificSchedule.start_time = JSON.stringify(startTime);
          this.specificSchedule.end_time = JSON.stringify(endTime);
          this.$emit('save-changes', this.specificSchedule);
        },

        checkDays() {
          if (this.courseSchedule?.days) {
            let stringDays = this.courseSchedule?.days;
            let daysAbrreviated = stringDays.split('|');

            this.selectedDays = daysAbrreviated.map(day => {
              switch(day.toLowerCase()) {
                case 'mo':
                  return 'Monday';
                case 'tu':
                  return 'Tuesday';
                case 'we':
                  return 'Wednesday';
                case 'th':
                  return 'Thursday';
                case 'fr':
                  return 'Friday';
                case 'sa':
                  return 'Saturday';
                case 'su':
                  return 'Sunday'
                default:
                  return day;
              }
            });
          }
        },

        checkTime() {
          if (this.courseSchedule?.start_time && this.courseSchedule?.end_time) {
            let startTime = this.courseSchedule?.start_time.split(':');
            let endTime = this.courseSchedule?.end_time.split(':');

            this.time.push(
              {
                hours: startTime[0],
                minutes: startTime[1],
                seconds: 0
              },
              {
                hours: endTime[0],
                minutes: endTime[1],
                seconds: 0
              },
            )
          }
        }
      },

      created() {
        this.checkDays();
        this.checkTime();
      }
  }
</script>

<style lang="scss" scoped>
    .card {
      width: 800px;
    }
</style>
