<template>
    <v-btn v-bind="$attrs">
        <slot />
    </v-btn>
</template>

<script>
    export default {
        name: 'Button',
    }
</script>

<style lang="scss" scoped>
    .v-btn {
        display: flex;
        min-width: 80px;
        padding: 10px;
        justify-content: center;
        align-items: center;
        gap: 10px;
        border-radius: 4px;
        text-transform: none;
        color: white;
        background: #1E65A3;
        letter-spacing: normal;
        box-shadow: none;

        &.primary {
            // default
        }

        &.secondary {
            color: #000;
            background: #ECF0F4;
        }

        &.tertiary {
            color: #000;
            background: #A1BAD0;
        }
    }
</style>
