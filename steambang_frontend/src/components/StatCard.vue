<script setup lang="ts">
import type { Component } from 'vue'

defineProps<{
  label: string
  value: string
  sub?: string
  icon: Component
  accent?: string
  glow?: string
}>()
</script>

<template>
  <div class="glass-card-hover p-5 group">
    <div class="flex items-start justify-between gap-3">
      <div>
        <p class="premium-label mb-2">{{ label }}</p>
        <p class="text-3xl font-bold tracking-tight">{{ value }}</p>
        <p v-if="sub" class="text-xs text-muted-foreground mt-2">{{ sub }}</p>
      </div>
      <div
        class="w-12 h-12 rounded-2xl flex items-center justify-center shrink-0 transition-transform group-hover:scale-105"
        :class="accent ?? 'bg-primary/15 text-primary border border-primary/20'"
        :style="glow ? { boxShadow: `0 0 20px ${glow}` } : undefined"
      >
        <component :is="icon" class="w-5 h-5" />
      </div>
    </div>
  </div>
</template>
