<template>
    <v-card class="card">
        <v-card-text v-if="!Object.keys(course).length">
          Create Course
        </v-card-text>
        <v-card-text v-else>
          Edit Course
        </v-card-text>
        <v-container>
            <v-row>
              <v-col
                cols="12"
                sm="6"
                md="4"
              >
                <v-text-field
                  label="Course Name*"
                  required
                  v-model="specificCourse.name"
                ></v-text-field>
              </v-col>
              <v-col
                cols="12"
                sm="6"
                md="4"
              >
                <v-text-field
                  label="Course Code*"
                  required
                  v-model="specificCourse.course_code"
                ></v-text-field>
              </v-col>
              <v-col
                cols="12"
                sm="6"
                md="4"
              >
                <v-text-field
                  label="Group Number*"
                  required
                  v-model="specificCourse.group_number"
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
                v-if="!Object.keys(course).length"
                color="blue-darken-1"
                variant="text"
                @click="$emit('add-course', specificCourse)"
            >
                Add Course
            </v-btn>
            <v-btn
                v-else
                color="blue-darken-1"
                variant="text"
                @click="$emit('save-changes', specificCourse)"
            >
                Save Changes
            </v-btn>
        </v-card-actions>
    </v-card>
</template>

<script>
export default{ 
    name: 'CreateEditCourse',
    props: {
        dialog: {
            type: Boolean,
            required: false,
        },

        course: {
          type: Object,
          required: true,
        }
    },

    data() {
      return {
        specificCourse: {
          id: this.course?.id ? this.course?.id : null,
          name: this.course?.name ? this.course?.name : null,
          course_code: this.course?.course_code ? this.course?.course_code : null,
          group_number: this.course?.group_number ? this.course?.group_number: null,
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
