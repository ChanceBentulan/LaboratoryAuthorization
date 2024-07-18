<template>
    <div
      ref="modal"
      :class="['modal', size, type]"
      @click="outsideClickHandler($event)"
    >
      <div class="modal-content">
        <div v-if="hasHeader" class="modal-header">
          <slot name="header" />
        </div>
        <div v-if="hasBody" class="modal-body">
          <slot name="body" />
        </div>
        <div v-if="hasFooter" class="modal-footer">
          <slot name="footer" />
        </div>
      </div>
    </div>
  </template>

  <script>
  export default {
    name: 'BaseModal',
    props: {
      size: {
        type: String,
        default: 'small',
      },
      type: {
        type: String,
        default: 'default',
      },
      allowOutsideClick: {
        type: Boolean,
        default: true,
      },
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
      },
    },
    methods: {
      outsideClickHandler(event) {
        if (this.allowOutsideClick && event.target === this.$refs.modal) {
          this.$emit('close');
        }
      },
    },
  };
  </script>

<style scoped lang="scss">
    $black: #0C0D0E;
    $white: #FFFFFF;
    $accent: #008FF5;
    $primary: $black;
    $secondary: #40484F;
    $tertiary: #67747E;
    $quaternary: #DDE1E3;
    $border: $quaternary;
    $error: #ED2B42;
    $success: #06B169;
    $warning: #F5C024;
    $disabled: #A0A9B1;
    // Highlight colors
    $accent-highlight: #DBEDFD;
    $primary-highlight: #EBEDEF;
    $error-highlight: #F6DADD;
    $success-highlight: #D8FEEE;
    $warning-highlight: #FBF4DB;
    // Container colors
    $accent-container: #EDF7FE;
    $primary-container: #F4F5F6;
    $error-container: #FAEDEE;
    $success-container: #EBFEF6;
    $warning-container: #FDF9ED;
    $light-container: #FAFAFA;

    $mobile: "screen and (max-width: 576px)";
    $tablet: "screen and (max-width: 768px)";

    $shadow-modal:
        0px 0px 0px 1px rgba($quaternary, 0.5),
        0px 4px 16px rgba($primary, 0.18),
        0px 24px 64px rgba($primary, 0.22);

    @mixin width-height($value) {
        width: $value;
        height: $value;
    }

    @mixin flex-align-center($direction: row) {
        display: flex;
        align-items: center;
        @if $direction == column {
            flex-direction: column;
        }
    }

    .modal-open {
        overflow: hidden;
    }

    .modal {
        position: fixed;
        z-index: 101;
        left: 0;
        top: 0;
        @include width-height(100%);
        overflow: auto;
        background: rgba($black, .3);

        &.tiny .modal-content {
            width: 360px;

            @media screen and (max-width: 840px) {
                width: 95%;
            }
        }
        &.small .modal-content,
        &.default .modal-content {
            width: 480px;

            @media #{$tablet} {
                width: 95%;
            }
        }

        &.medium .modal-content {
            width: 640px;

            @media #{$tablet} {
                width: 95%;
            }
        }

        &.large .modal-content {
            width: 840px;

            @media #{$tablet} {
                width: 95%;
            }
        }

        &.Xlarge .modal-content {
            width: 1040px;

            @media #{$tablet} {
                width: 95%;
            }
        }

        &.unclip .modal-content {
            overflow: initial;
        }

        .video-content {
            margin: 0 auto;
            color: $white;

            @media #{$mobile} {
                margin: 16px auto;
            }
        }
    }

    .modal-content {
        background: $white;
        margin: 48px auto;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: $shadow-modal;

        @media #{$mobile} {
            margin: 16px auto;
        }
    }

    .modal-loading {
        .spinner {
            margin: 32px;
        }

        & ~ * {
            display: none !important;
        }
    }

    .modal-header {
        position: relative;
        width: 100%;
        padding: 20px 24px 0;

        .header-title {
            font-size: 20px;
            font-weight: bold;
            letter-spacing: -0.02rem;
            color: $primary;
        }

        .header-subtitle {
            color: $secondary;
        }

        .header-wrapper {
            & > * + * {
                margin-top: 4px;
            }
        }

        .header-action-wrapper {
            display: flex;
            align-items: flex-start;

            .header-title {
                flex: 1;
            }

            .header-wrapper {
                flex: 1;
                padding-right: 8px;

                .header-title {
                    flex: 0;
                }
            }
        }

        .header-avatar-wrapper {
            display: flex;

            .avatar + .header-wrapper,
            .avatar + .header-title,
            .sign + .header-wrapper,
            .sign + .header-title {
                padding-left: 12px;
                flex: 1;
            }

            .avatar + .header-title,
            .sign + .header-title {
                align-self: center;
            }
        }
    }

    .modal-body,
    .modal-body-alt {
        position: relative;
        padding: 20px 24px;

        .warning-text {
            color: $error;
        }

        .blue-text {
            color: $accent;
        }

        .alert {
            margin-bottom: 8px;
        }

        > * {
            margin-bottom: 8px;

            &:last-child {
                margin-bottom: 0;
            }
        }

        .subheader-title {
            font-size: 16px;
            color: $secondary;
            margin-bottom: 16px;
        }

        .subheader-subtitle {
            font-size: 14px;
            color: $secondary;
            margin-bottom: 16px;
        }

        .subheader-wrapper {
            margin-bottom: 16px;

            .subheader-title,
            .subheader-subtitle {
                margin-bottom: 0;
            }

            :not(:first-child) {
                padding-top: 2px;
            }
        }

        .subheader-action-wrapper {
            display: flex;
            margin-bottom: 16px;

            .subheader-title {
                flex: 1;
            }

            .subheader-wrapper {
                flex: 1;
                padding-right: 8px;
                margin-bottom: 0;

                .subheader-title {
                    flex: 0;
                }
            }

            a {
                text-decoration: none;
                cursor: pointer;
            }
        }

        .control-group {
            margin-bottom: 20px;
            padding-top: 12px;

            &:first-child {
                padding-top: 0;
            }

            &:last-child {
                margin-bottom: 0;
            }

            .control-group-header .subheader-wrapper,
            .control-group-header .subheader-action-wrapper,
            .control-group-header .subheader-title,
            .control-group-header .subheader-subtitle {
                margin-bottom: 0;
            }

            .control-group-header + .control-group-body {
                padding-top: 16px;
            }
        }
    }

    .modal-footer {
        display: flex;
        justify-content: space-between;
        padding: 20px 24px;
        background: $light-container;
        border-top: 1px solid $border;
        border-radius: 0 0 8px 8px;

        .footer-left {
            margin-right: auto;
            @include flex-align-center();
            gap: 12px;
        }

        .footer-block {
            width: 100%;
            display: flex;
            gap: 12px;

            button{
                flex: 1;
            }
        }

        .footer-right {
            margin-left: auto;
            @include flex-align-center();
            gap: 12px;
        }

        .footer-stack {
            @include flex-align-center();
            flex-direction: column;
            gap: 12px;
            width: 100%;

            button + button {
                margin-left: 0;
            }
            a {
                display: block;
            }
        }
    }
</style>