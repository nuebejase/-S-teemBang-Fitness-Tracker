<script setup lang="ts">
import { ref, watch } from 'vue'
import Card from '@/components/ui/Card.vue'
import TrendChart from '@/components/TrendChart.vue'
import { useAppStore } from '@/stores/appStore'

const store = useAppStore()
const metric = ref<'steps' | 'calories' | 'workouts'>('steps')
const days = ref(14)

watch(days, async (d) => {
  await store.refreshTrends(d)
})

async function load() {
  await store.refreshTrends(days.value)
}
void load()
</script>

<template>
  <div class="container mx-auto px-4 py-8 space-y-6 max-w-4xl">
    <div>
      <h1 class="text-2xl font-bold tracking-tight">Analytics</h1>
      <p class="text-muted-foreground text-sm mt-1">Track your progress over time.</p>
    </div>
    <div class="flex flex-wrap gap-3">
      <select v-model="metric" class="premium-select w-auto min-w-[140px]">
        <option value="steps">Steps</option>
        <option value="calories">Calories</option>
        <option value="workouts">Workouts</option>
      </select>
      <select v-model.number="days" class="premium-select w-auto min-w-[120px]">
        <option :value="7">7 days</option>
        <option :value="14">14 days</option>
        <option :value="30">30 days</option>
      </select>
    </div>
    <Card class="p-6">
      <TrendChart v-if="store.trends.length" :points="store.trends" :metric="metric" />
      <p v-else class="text-muted-foreground text-sm text-center py-8">No trend data yet.</p>
    </Card>
    <div class="grid sm:grid-cols-3 gap-4">
      <Card class="p-4 text-center">
        <p class="premium-label mb-2">Week steps</p>
        <p class="text-2xl font-bold">{{ store.dashboard?.weekSteps ?? 0 }}</p>
      </Card>
      <Card class="p-4 text-center">
        <p class="premium-label mb-2">Week calories</p>
        <p class="text-2xl font-bold">{{ store.dashboard?.weekCalories ?? 0 }}</p>
      </Card>
      <Card class="p-4 text-center">
        <p class="premium-label mb-2">Week workouts</p>
        <p class="text-2xl font-bold">{{ store.dashboard?.weekWorkouts ?? 0 }}</p>
      </Card>
    </div>
  </div>
</template>
