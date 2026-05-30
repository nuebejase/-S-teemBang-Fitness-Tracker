<script setup lang="ts">
import { computed } from 'vue'
import type { Component } from 'vue'

const props = withDefaults(
  defineProps<{
    value: number
    max: number
    label: string
    sublabel?: string
    icon: Component
    color?: 'emerald' | 'orange' | 'blue' | 'violet'
    size?: 'sm' | 'md'
  }>(),
  { color: 'emerald', size: 'md' },
)

const progress = computed(() => (props.max > 0 ? Math.min(100, Math.round((props.value / props.max) * 100)) : 0))

const ringSize = props.size === 'sm' ? 'w-24 h-24' : 'w-32 h-32'
const innerSize = props.size === 'sm' ? 'inset-1.5' : 'inset-2'

const gradient = {
  emerald: 'from-emerald-500 to-teal-400',
  orange: 'from-orange-500 to-amber-400',
  blue: 'from-blue-500 to-cyan-400',
  violet: 'from-violet-500 to-purple-400',
}[props.color]

const iconColor = {
  emerald: 'text-emerald-400',
  orange: 'text-orange-400',
  blue: 'text-blue-400',
  violet: 'text-violet-400',
}[props.color]

const ringColor = {
  emerald: 'hsl(158 64% 52%)',
  orange: 'hsl(25 95% 53%)',
  blue: 'hsl(217 91% 60%)',
  violet: 'hsl(262 83% 65%)',
}[props.color]
</script>

<template>
  <div class="flex flex-col items-center gap-2">
    <div :class="['relative rounded-full flex items-center justify-center shrink-0', ringSize]" :style="{ '--progress': `${progress}%`, '--ring-color': ringColor }">
      <div class="absolute inset-0 rounded-full progress-ring" />
      <div :class="['absolute rounded-full bg-card flex flex-col items-center justify-center', innerSize]">
        <component :is="icon" :class="['mb-0.5', iconColor, size === 'sm' ? 'w-4 h-4' : 'w-5 h-5']" />
        <span :class="size === 'sm' ? 'text-lg font-bold' : 'text-xl font-bold'">{{ Math.round(value) }}</span>
      </div>
    </div>
    <div class="text-center">
      <p class="text-xs font-semibold uppercase tracking-wider text-muted-foreground">{{ label }}</p>
      <p v-if="sublabel" class="text-[10px] text-muted-foreground mt-0.5">{{ sublabel }}</p>
      <div class="mt-2 h-1.5 w-20 mx-auto rounded-full bg-muted overflow-hidden">
        <div :class="['h-full rounded-full bg-gradient-to-r transition-all duration-700', gradient]" :style="{ width: `${progress}%` }" />
      </div>
      <p class="text-[10px] text-muted-foreground mt-1">{{ progress }}%</p>
    </div>
  </div>
</template>

<style scoped>
.progress-ring {
  background: conic-gradient(
    var(--ring-color) var(--progress, 0%),
    hsl(222 30% 14%) var(--progress, 0%)
  );
}
</style>
