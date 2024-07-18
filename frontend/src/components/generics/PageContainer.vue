<template>
    <div class="page-container">
        <div class="content-sticky">
            <div class="header-container">
                <div class="title-container">
                    <h1>
                        {{ title }}
                    </h1>
                    <p v-if="subTitle">
                        {{ subTitle }}
                    </p>
                </div>
                <!-- WIP, Not yet needed -->
                <!-- <div class="actions"></div>  -->
            </div>
        </div>
        <div class="content-container">
            <slot />
        </div>
    </div>
</template>

<script>
    export default {
        name: 'PageContainer',

        props: {
            title: {
                type: String,
                default: 'Page Title'
            },

            subTitle: String
        },

        computed: {
            hasHeader() {
                return !!this.$slots.header;
            },

            hasBody() {
                return !!this.$slots.body;
            },

            hasFooter() {
                return !!this.$slots.footer;
            }
        }
    }
</script>

<style lang="scss" scoped>

    .content-sticky {
        border-bottom: 1px solid #DDE1E3;
        background: #F7F8F9;
        position: sticky;
        padding: 24px 80px;
        z-index: 4;

        .header-container {
            display: flex;
            align-items: center;
            gap: 12px;

            h1 {
                flex: 1;
                font-size: 20px;
            }

            p {
                color: #67747E;
            }

            .title-container{
                flex: 1;

                & > * + * {
                    margin-top: 4px;
                }

                h1 {
                    flex: unset;
                }

                button {
                    width: min-content;
                }
            }

            .actions {
                display: inline-flex;
                gap: 12px;
            }
        }
    }

    .content-container {
        padding: 40px 80px;
    }
</style>