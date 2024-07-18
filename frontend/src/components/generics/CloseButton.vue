<template>
    <Button
        class="secondary"
        :class="['type-'+type]"
        :disabled="disabled"
        @click="$emit('close')"
    >
        <i class="mdi mdi-close"></i>
    </Button>
</template>

<script>
    import Button from './Button.vue';

    export default {
        name: 'CloseButton',

        components: {
            Button
        },

        props: {
            type: {
                type: String,
                required: false
            },

            disabled: {
                type: Boolean,
                default: false
            }
        }
    };
</script>

<style scoped lang="scss">
    $tertiary: #67747E;
    $error: #ED2B42;
    $white: #FFFFFF;

    .v-btn {
        min-width: unset;
    }

    button {
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 100% !important;

        i {
            font-size: 20px;
        }

        &.type-text-field {
            width: 26px !important;
            height: 26px !important;
            border-radius: 28px;

            i {
                font-size: 17px;
            }
        }

        &.type-modal {
            position: absolute;
            top: 20px;
            right: 24px;
            width: 22px !important;
            height: 22px !important;
            z-index: 1;

            i {
                font-size: 20px;
                color: $tertiary;
                // Temporary, to investigate (Drix)
                margin-left: -2px;
            }

            &:hover {
                background: $error;

                i {
                    color: $white;
                }
            }
        }

        &.type-panel {
            width: 32px !important;
            height: 32px !important;
            border-radius: 4px !important;

            i {
                font-size: 20px !important;
                color: $tertiary;
            }
        }
    }
</style>
