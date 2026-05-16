<script setup lang="ts">
import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import { useAppStore } from '@/stores/appStore'
import { formatDateTime, formatNumber } from '@/lib/utils'
import { toast } from 'vue-sonner'
import { Trash2 } from 'lucide-vue-next'

const store = useAppStore()

async function remove(id: string) {
  try {
    await store.removeActivity(id)
    toast.success('Activity removed')
  } catch (e) {
    toast.error(e instanceof Error ? e.message : 'Delete failed')
  }
}
</script>

<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-2xl font-bold mb-6">Activity history</h1>
    <p v-if="!store.activities.length" class="text-muted-foreground">No activities yet. Log a workout or sync steps.</p>
    <div v-else class="space-y-3 max-w-2xl">
      <Card v-for="a in store.activities" :key="a.id" class="p-4 flex gap-4 justify-between items-start">
        <div>
          <p class="font-semibold">{{ a.title }}</p>
          <p class="text-sm text-muted-foreground capitalize">
            {{ a.activityType }} · {{ a.category }} · {{ formatDateTime(a.loggedAt) }}
          </p>
          <p class="text-sm mt-2">
            <span v-if="a.steps">{{ formatNumber(a.steps) }} steps · </span>
            <span v-if="a.durationMinutes">{{ a.durationMinutes }} min · </span>
            {{ a.caloriesBurned }} kcal
          </p>
        </div>
        <Button variant="ghost" size="icon" aria-label="Delete" @click="remove(a.id)">
          <Trash2 class="w-4 h-4 text-red-500" />
        </Button>
      </Card>
    </div>
  </div>
</template>
