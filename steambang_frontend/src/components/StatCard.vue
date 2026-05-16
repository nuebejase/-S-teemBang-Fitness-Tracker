<script setup lang="ts">
import Card from '@/components/ui/Card.vue'
import type { Component } from 'vue'

defineProps<{
  label: string
  value: string
  sub?: string
  icon: Component
  accent?: string
}>()
</script>

<template>
  <Card class="p-5">
    <div class="flex items-start justify-between gap-3">
      <div>
        <p class="text-sm text-muted-foreground">{{ label }}</p>
        <p class="text-2xl font-bold mt-1">{{ value }}</p>
        <p v-if="sub" class="text-xs text-muted-foreground mt-1">{{ sub }}</p>
      </div>
      <div
        class="w-11 h-11 rounded-xl flex items-center justify-center shrink-0"
        :class="accent ?? 'bg-primary/10 text-primary'"
      >
        <component :is="icon" class="w-5 h-5" />
      </div>
    </div>
  </Card>
</template>
