// store.js
import { createStore } from 'vuex';
import axios from '../axios/axios';

const store = createStore({
    state() {
      return {
        masterList: null,
        courses: null,
        courseSchedules: null,
        usersInSchedule: null,
        user: null,
        schedulesToday: null,
      };
    },
    mutations: {
        // User

        setUserData(state, payload) {
            state.user = payload;
        },

        // MasterList
        setMasterlistData(state, payload) {
            state.masterList = payload;
        },

        addMasterlistData(state, payload) {
            state.masterList.push(payload);
        },

        removeMasterlistData(state, payload) {
            state.masterList = state.masterList.filter(obj => obj.id !== payload);
        },

        updateMasterlistData(state, payload) {
            let index = state.masterList.findIndex(item => item.id === payload.id);

            if (index !== -1) {
                state.masterList.splice(index, 1, payload);
            }
        },

        // Courses
        setCoursesData(state, payload) {
            state.courses = payload;
        },

        addCoursesData(state, payload) {
            state.courses.push(payload);
        },

        removeCourseData(state, payload) {
            state.courses = state.courses.filter(obj => obj.id !== payload);
        },

        updateCourseData(state, payload) {
            let index = state.courses.findIndex(item => item.id === payload.id);

            if (index !== -1) {
                state.courses.splice(index, 1, payload);
            }
        },

        // Schedules
        setCourseSchedulesData(state, payload) {
            state.courseSchedules = payload;
        },

        addCourseSchedulesData(state, payload) {
            state.courseSchedules.push(payload);
        },

        removeCourseSchedulesData(state, payload) {
            state.courseSchedules = state.courseSchedules.filter(obj => obj.id !== payload);
        },

        updateCourseSchedulesData(state, payload) {
            let index = state.courseSchedules.findIndex(item => item.id === payload.id);

            if (index !== -1) {
                state.courseSchedules.splice(index, 1, payload);
            }
        },

        setUsersInSchedule(state, payload) {
            state.usersInSchedule = payload;
        },

        setSchedulesToday(state, payload) {
            state.schedulesToday = payload;
        }
    },
    actions: {
        async loginUser({commit}, payload) {
            try {
                const response = await axios.post('/api/login', payload);
                localStorage.setItem('token', response.data.token);
                commit('setUserData', response.data.user);
                localStorage.setItem('full_name', response.data.user.full_name);
                localStorage.setItem('user_type', response.data.user.user_type);
                localStorage.setItem('user_id', response.data.user.id);
                return response.status;
            } catch(error) {
                console.error('Error logging in:', error);
            }
        },

        async fetchMasterList({commit}) {
            try {
                const response = await axios.get('/api/users');
                commit('setMasterlistData', response.data);
            } catch (error) {
                console.error('Error fetching data: ', error)
            }
        },

        async createUser({commit}, payload) {
            try {
                const response = await axios.post('/api/users', payload);
                commit('addMasterlistData', response.data)
            } catch(error) {
                console.error('Error creating user:', error)
            }
        },

        async deleteUser({commit}, payload) {
            try {
                await axios.delete(`/api/user/${payload}`);
                commit('removeMasterlistData', payload)
            } catch(error) {
                console.error('Error deleting user:', error)
            }
        },

        async updateUser({commit}, payload) {
            try {
                const response  = await axios.patch(`/api/user/${payload.id}`, payload);
                commit('updateMasterlistData', response.data)
            } catch(error) {
                console.error('Error updating data:', error);
            }
        },

        async fetchCourses({commit}) {
            try {
                const response = await axios.get('/api/courses');
                commit('setCoursesData', response.data);
            } catch (error) {
                console.error('Error fetching data: ', error)
            }
        },

        async createCourse({commit}, payload) {
            try {
                const response = await axios.post('/api/courses', payload);
                commit('addCoursesData', response.data)
            } catch(error) {
                console.error('Error creating Course:', error)
            }
        },

        async deleteCourse({commit}, payload) {
            try {
                await axios.delete(`/api/course/${payload}`);
                commit('removeCourseData', payload)
            } catch(error) {
                console.error('Error deleting course:', error)
            }
        },

        async updateCourse({commit}, payload) {
            try {
                const response  = await axios.patch(`/api/course/${payload.id}`, payload);
                commit('updateCourseData', response.data)
            } catch(error) {
                console.error('Error updating data:', error);
            }
        },

        async fetchCourseSchedules({commit}) {
            try {
                const response = await axios.get(
                    '/api/course-schedules');
                commit('setCourseSchedulesData', response.data);
            } catch (error) {
                console.error('Error fetching data: ', error)
            }
        },

        async createCourseSchedule({commit}, payload) {
            try {
                const response = await axios.post(
                    '/api/course-schedules', payload);
                commit('addCourseSchedulesData', response.data)
            } catch(error) {
                console.error('Error creating course schedule:', error)
            }
        },

        async deleteCourseSchedule({commit}, payload) {
            try {
                await axios.delete(
                    `/api/course-schedule/${payload}`);
                commit('removeCourseSchedulesData', payload)
            } catch(error) {
                console.error('Error deleting course schedule:', error)
            }
        },

        async updateCourseSchedule({commit}, payload) {
            try {
                const response = await axios.patch(
                    `/api/course-schedule/${payload.id}`, payload);
                commit('updateCourseSchedulesData', response.data)
            } catch(error) {
                console.error('Error updating data:', error);
            }
        },

        async addUsersToSchedule ({commit}, payload) {
            try {
                const response = await axios.patch(`/api/user-course-schedule/${payload.course_schedule_id}`, payload);
            } catch(error) {
                console.error('Error updating data: ', error);
            }
        },

        async fetchSpecificCourseSchedule( {commit}, payload ) {
            try {
                const response = await axios.get(`/api/course-schedule/${payload}`);
                commit('updateCourseSchedulesData', response.data);
            } catch(error) {
                console.error('Error getting data: ', error)
            }
        },

        async fetchSpecificUser( {commit}, payload ) {
            const response = await axios.get(`/api/user/${payload}`);
            commit('setUserData', response.data);
        },

        async updateUserInformation( {commit}, payload ) {
            const response = await axios.patch(
                `/api/update-user-information/${payload.id}`, payload);
            return response.status;
        },

        async fetchUsersInSchedule ({commit}, payload) {
            try {
                const response = await axios.get(`/api/users-schedule/${payload}`, )
                commit('setUsersInSchedule', response.data)
            } catch(error) {
                console.error('Error updating data: ', error);
            }
        },

        async uploadCSVFile ({commit}, formData) {
            try {
                const response = await axios.post(`/api/upload-csv`, formData);
                return response.data.message
            } catch(error) {
                console.error('Error uploading csv', error);
            }
        },

        async registerUser({commit}, payload) {
            try {
                const response = await axios.post(`/api/register`, payload);
                return response;
            } catch(error) {
                console.error('Error registering account', error);
            }
        },

        async fetchScheduleToday({commit}, payload) {
            try {
                const response = await axios.get(`/api/schedules-today`);
                commit('setSchedulesToday', response.data);
            } catch(error) {
                console.error('Error fetching schedule today')
            }
        }
    },

    getters: {
        masterList: state => state.masterList,
    }
  });
  
  export default store;