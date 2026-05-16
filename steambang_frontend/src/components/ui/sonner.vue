<script setup lang="ts">
import { Toaster } from 'vue-sonner'

withDefaults(defineProps<{ position?: 'top-center' | 'top-right' }>(), { position: 'top-center' })
</script>

<template>
  <Toaster :position="position" rich-colors />
</template>
