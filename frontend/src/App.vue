<template>
    <v-app class="app">
        <div v-if="!isLoading">
            <v-navigation-drawer
                v-if="computedShowNavigationDrawer"
                app
            >
                <Sidebar @signout="signOutUser"/>
            </v-navigation-drawer>
            <v-main>
                <router-view @signed-in="handleSignin"/>
            </v-main>
        </div>
  </v-app>
</template>

<script>
    import Sidebar from './components/Sidebar.vue'
    import BaseModal from './components/generics/BaseModal.vue'
    import Button from './components/generics/Button.vue'
    import CloseButton from './components/generics/CloseButton.vue'

    export default {
        name: 'App',

        emits: ['signed-in'],

        components: {
            Sidebar,
            BaseModal,
            Button,
            CloseButton
        },

        data() {
            return {
                showNavigationDrawer: false,
                isLoading: false,
            };
        },

        computed: {
            computedShowNavigationDrawer() {
                return this.$route.meta.showNavigationDrawer || this.showNavigationDrawer;
            }
        },

        methods: {
            handleSignin(value) {
                this.isLoading = true;
                this.$nextTick(() => {
                    this.$router.push({
                        name: 'dashboard'
                    });
                    this.$route.meta.showNavigationDrawer = true;
                    this.showNavigationDrawer = value;
                });
                this.isLoading = false;
            },

            signOutUser() {
                localStorage.clear();
                this.$router.push({
                        name: 'sign-in'
                    });
                this.showNavigationDrawer = false;
            }
        }
    }
</script>

<style lang="scss" scoped>
    :deep(.v-navigation-drawer__wrap) {
        display: grid;
        grid-template-columns: auto 1fr;
    }

    .sign-out-button {
        display: flex;
        justify-content: flex-end;
        margin-top: 20px;
    }

    .sign-out-button Button.secondary {
        margin-right: 15px; 
    }
</style>
