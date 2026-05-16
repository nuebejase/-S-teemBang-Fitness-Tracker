<script setup lang="ts">
import { ref } from 'vue'
import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import { useAppStore } from '@/stores/appStore'
import { formatNumber } from '@/lib/utils'
import { toast } from 'vue-sonner'
import { Trash2 } from 'lucide-vue-next'

const store = useAppStore()
const metric = ref<'steps' | 'calories' | 'workouts'>('steps')
const period = ref<'daily' | 'weekly' | 'monthly'>('daily')
const target = ref(8000)

async function add() {
  try {
    await store.addGoal(metric.value, period.value, target.value)
    toast.success('Goal created')
  } catch (e) {
    toast.error(e instanceof Error ? e.message : 'Failed')
  }
}

async function remove(id: string) {
  try {
    await store.removeGoal(id)
    toast.success('Goal removed')
  } catch (e) {
    toast.error(e instanceof Error ? e.message : 'Failed')
  }
}
</script>

<template>
  <div class="container mx-auto px-4 py-8 max-w-2xl">
    <h1 class="text-2xl font-bold mb-6">Fitness goals</h1>
    <Card class="p-6 mb-8 space-y-4">
      <h2 class="font-semibold">New goal</h2>
      <div class="grid sm:grid-cols-3 gap-3">
        <div>
          <label class="text-xs font-medium">Metric</label>
          <select v-model="metric" class="mt-1 w-full px-3 py-2 rounded-lg border">
            <option value="steps">Steps</option>
            <option value="calories">Calories</option>
            <option value="workouts">Workouts</option>
          </select>
        </div>
        <div>
          <label class="text-xs font-medium">Period</label>
          <select v-model="period" class="mt-1 w-full px-3 py-2 rounded-lg border">
            <option value="daily">Daily</option>
            <option value="weekly">Weekly</option>
            <option value="monthly">Monthly</option>
          </select>
        </div>
        <div>
          <label class="text-xs font-medium">Target</label>
          <input v-model.number="target" type="number" min="1" class="mt-1 w-full px-3 py-2 rounded-lg border" />
        </div>
      </div>
      <Button @click="add">Add goal</Button>
    </Card>
    <div class="space-y-3">
      <Card v-for="g in store.goals" :key="g.id" class="p-4 flex justify-between items-start gap-4">
        <div class="flex-1">
          <p class="font-semibold capitalize">{{ g.period }} {{ g.metric }}</p>
          <p class="text-sm text-muted-foreground">
            {{ formatNumber(g.currentValue) }} / {{ formatNumber(g.targetValue) }}
          </p>
          <div class="mt-2 h-2 w-full max-w-xs rounded-full bg-muted overflow-hidden">
            <div class="h-full bg-emerald-500" :style="{ width: `${g.progressPercent}%` }" />
          </div>
        </div>
        <Button variant="ghost" size="icon" @click="remove(g.id)"><Trash2 class="w-4 h-4 text-red-500" /></Button>
      </Card>
    </div>
  </div>
</template>
