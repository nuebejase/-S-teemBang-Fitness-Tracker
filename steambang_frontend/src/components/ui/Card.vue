<script setup lang="ts">
import { computed } from 'vue'
import { cn } from '@/lib/utils'

const props = defineProps<{ class?: string; glass?: boolean }>()
const className = computed(() =>
  cn(
    props.glass !== false
      ? 'glass-card text-card-foreground'
      : 'rounded-2xl border bg-card text-card-foreground shadow-sm',
    props.class,
  ),
)
</script>

<template>
  <div :class="className">
    <slot />
  </div>
</template>
