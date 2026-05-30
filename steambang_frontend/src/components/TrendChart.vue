<script setup lang="ts">
import { computed } from 'vue'
import type { TrendPoint } from '@/types/domain'
import { formatNumber } from '@/lib/utils'

const props = defineProps<{
  points: TrendPoint[]
  metric: 'steps' | 'calories' | 'workouts'
}>()

const values = computed(() =>
  props.points.map((p) => (props.metric === 'steps' ? p.steps : props.metric === 'calories' ? p.calories : p.workouts)),
)

const max = computed(() => Math.max(...values.value, 1))

function barHeight(v: number) {
  return `${Math.max(8, (v / max.value) * 100)}%`
}

function label(d: string) {
  const dt = new Date(d + 'T12:00:00')
  return dt.toLocaleDateString(undefined, { weekday: 'short' }).slice(0, 3)
}
</script>

<template>
  <div class="flex items-end gap-1.5 h-40" role="img" :aria-label="`${metric} trend chart`">
    <div v-for="(p, i) in points" :key="p.date" class="flex-1 flex flex-col items-center gap-1 min-w-0">
      <span class="text-[10px] text-muted-foreground truncate w-full text-center" :title="String(values[i])">
        {{ values[i] > 0 ? formatNumber(values[i]) : '' }}
      </span>
      <div
        class="w-full rounded-t-lg bg-gradient-to-t from-emerald-600 to-emerald-400/80 transition-all duration-500 hover:from-emerald-500"
        :style="{ height: barHeight(values[i]) }"
      />
      <span class="text-[10px] text-muted-foreground">{{ label(p.date) }}</span>
    </div>
  </div>
</template>
