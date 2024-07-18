<template>
    <div class="sidebar">
        <section class="avatar-container">
            <div class="avatar-container__info">
                <p class="name">
                    {{ full_name }}
                </p>
                <p class="user-type">
                    {{ user_type }}
                </p>
            </div>
        </section>
        <ul class="sidebar-list">
            <li @click="goTo('dashboard')">Dashboard</li>
            <li @click="goTo('masterlist')">Master List</li>
            <li @click="goTo('courses')">Courses</li>
            <li @click="goTo('schedules')">Schedules</li>
            <li
                v-if="user_type==='administrator'"
                @click="goTo('register')"
            >
                Register Account
            </li>
            <li @click="goTo('settings')">User Settings</li>
            <div class="spacer"/>
            <li @click="$emit('signout')">Sign Out</li>
        </ul>
    </div>
</template>

<script>
    import { mapState } from 'vuex';

    export default {
        name: 'Sidebar',

        data() {
            return {
                full_name: '',
                user_type: ''
            }
        },

        methods: {
            goTo(routeName) {
                this.$router.push({
                    name: routeName,
                });
            }
        },

        created() {
            this.full_name = localStorage.getItem('full_name');
            this.user_type = localStorage.getItem('user_type');
        }
    }
</script>

<style lang="scss" scoped>
    .sidebar {
        background: #1D3244;
        color: white;
        padding: 12px;
        display: flex;
        flex-direction: column;
        height: inherit;
        width: 240px;

        &-list {
            display: flex;
            flex-direction: column;
            padding: 0;
            margin: 0;
            height: 100%;

            li {
                padding: 8px 12px;
                border-radius: 8px;
                min-height: unset;
                list-style: none;
                cursor: pointer;

                &:hover {
                    background: rgba(255, 255, 255, 0.10);;
                }
            }

            .spacer {
                flex: 1;
                // height: 100%;
            }
        }

        .avatar-container {
            display: flex;
            align-items: center;
            padding: 12px 12px;
            gap: 8px;

            &__image {
                border-radius: 50%;
                width: 32px;
                height: 32px;
            }

            &__info {
                display: flex;
                flex-direction: column;
                gap: 2px;

                .name {
                    font-size: 14px;
                    font-weight: 600;
                }

                .user-type {
                    font-size: 13px;
                    font-weight: 400;
                    overflow: hidden;
                    display: -webkit-box;
                    -webkit-line-clamp: 1;
                    -webkit-box-orient: vertical;
                }
            }
        }
    }
</style>