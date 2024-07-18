<template>
    <div class="sign-in">
        <section class="header">
            <p class="header__text">
                SECN User Management System
            </p>
        </section>
        <main class="container">
            <img src="../assets/secn-logo.png" alt="SECN Logo" />
            <v-form class="input-container">
                <div class="input-container">
                <label for="id-number">username</label>
                <input type="text" placeholder="Enter Username" v-model="username">
                </div>
                <div class="input-container">
                    <label for="password">Password</label>
                    <input type="password" placeholder="Enter Password" autocomplete="on" v-model="password" @keyup.enter="validateLogin">
                </div>
            </v-form>
            <p 
                class="error"
                v-if="showError"
            >
                Invalid username or password
            </p>
            <Button
                class="button"
                @click="validateLogin"
            >
                Sign In
            </Button>
        </main>
        <footer class="footer">
        </footer>
    </div>
</template>

<script>
    import Button from '../components/generics/Button.vue'
    import { mapActions } from 'vuex';

    export default {
        name: 'SignInPage',

        components: {
            Button
        },

        data() {
            return {
                username: '',
                password: '',
                showError: false,
            }
        },

        methods: {
            ...mapActions(['loginUser'],),

            async validateLogin() {
                let payload = {
                    username: this.username,
                    password: this.password
                }
                let response = await this.loginUser(payload);
                if (response === 200) {
                    this.$emit('signed-in', true);
                } else {
                    this.showError = true;
                }
            }
        }
    }
</script>

<style lang="scss" scoped>
    *,
    body {
        margin: 0;
        padding: 0;
    }

    .header {
        padding: 18px 12px;
        background: #1E65A3;
        position: fixed;
        top: 0;
        width: 100%;

        &__text {
            font-weight: 700;
            color: #fff;
        }
    }

    .container {
        width: 340px;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 24px;
        margin: 89px auto;

        img {
            height: 80px;
            width: 80px;
        }

        .error {
            color: red;
        }
    }

    .input-container {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        gap: 4px;
        width: 100%;
    }

    input {
        border-radius: 4px;
        border: 1px solid var(--background-border, #DDE1E3);
        display: flex;
        padding: 8px 12px;
        align-items: center;
        align-self: stretch;
    }

    button {
        display: flex;
        min-width: 80px;
        padding: 10px;
        justify-content: center;
        align-items: center;
        gap: 10px;
        align-self: stretch;
        border-radius: 4px;
        background-color: #1E65A3;
        color: #fff;
        min-width: 140px;
        border: none;
        cursor: pointer;

        &:hover {
            background-color: #1a4f7e;
        }
    }

    footer {
        background-color: #F4F5F6;
        border-top: 1px solid #DDE1E3;
        list-style: none;
        position: fixed;
        bottom: 0;
        width: 100%;
        display: flex;
        padding: 16px 12px;
        flex-direction: column;
        align-items: center;
        gap: 8px;

        li {
            display: flex;
            gap: 10px;
            padding: 4px;
            align-items: center;
            justify-content: center;
        }

        .icon {
            width: 20px;
            height: 20px;
        }
    }
</style>
