<script setup lang="ts">
import { Toaster } from 'vue-sonner'

type ToastPosition =
  | 'top-left'
  | 'top-right'
  | 'bottom-left'
  | 'bottom-right'
  | 'top-center'
  | 'bottom-center'

withDefaults(
  defineProps<{
    position?: ToastPosition
  }>(),
  { position: 'top-right' },
)
</script>

<template>
  <Toaster :position="position" />
</template>
