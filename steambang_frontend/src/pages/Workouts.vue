<script setup lang="ts">
import { computed, ref } from 'vue'
import { RouterLink } from 'vue-router'
import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import { useWorkoutTimer } from '@/composables/useWorkoutTimer'
import { useAppStore } from '@/stores/appStore'
import { toast } from 'vue-sonner'
import { Play, Square, Timer, History } from 'lucide-vue-next'

const store = useAppStore()
const { running, formatted, elapsedMinutes, elapsedSeconds, start, stop, reset } = useWorkoutTimer()
const category = ref('running')
const title = ref('')
const duration = ref(30)
const notes = ref('')
const saving = ref(false)
const useTimerMode = ref(true)

const categories = ['running', 'walking', 'cycling', 'strength', 'yoga', 'hiit', 'swimming', 'other']

const recentWorkouts = computed(() =>
  store.activities.filter((a) => a.activityType === 'workout').slice(0, 5),
)

async function submitManual() {
  if (duration.value < 1) {
    toast.error('Duration must be at least 1 minute')
    return
  }
  saving.value = true
  try {
    const created = await store.logWorkout({
      category: category.value,
      title: title.value || `${category.value} workout`,
      durationMinutes: duration.value,
      notes: notes.value,
    })
    toast.success(`Workout saved — ${created.caloriesBurned} kcal burned`)
    title.value = ''
    notes.value = ''
  } catch (e) {
    toast.error(e instanceof Error ? e.message : 'Failed to log workout')
  } finally {
    saving.value = false
  }
}

async function submitFromTimer() {
  stop()
  if (elapsedSeconds.value === 0) {
    toast.error('Start the timer first')
    return
  }
  saving.value = true
  try {
    const mins = elapsedMinutes.value
    const created = await store.logWorkout({
      category: category.value,
      title: title.value || `${category.value} workout`,
      durationMinutes: mins,
      notes: notes.value || `Timed session — ${formatted.value}`,
    })
    toast.success(`Workout saved — ${mins} min, ${created.caloriesBurned} kcal`)
    reset()
    title.value = ''
    notes.value = ''
  } catch (e) {
    toast.error(e instanceof Error ? e.message : 'Failed')
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <div class="container mx-auto px-4 py-8 max-w-xl space-y-6">
    <div>
      <h1 class="text-2xl font-bold tracking-tight">Log workout</h1>
      <p class="text-muted-foreground text-sm mt-1">
        Saved workouts appear on your home dashboard, goals, and
        <RouterLink to="/activities" class="text-emerald-400 hover:underline">activity history</RouterLink>.
      </p>
    </div>

    <div class="flex gap-2 p-1 rounded-xl bg-white/[0.04] border border-white/10">
      <button
        type="button"
        class="flex-1 py-2 rounded-lg text-sm font-medium transition-all"
        :class="useTimerMode ? 'bg-emerald-500/20 text-emerald-300' : 'text-muted-foreground'"
        @click="useTimerMode = true"
      >
        <Timer class="w-4 h-4 inline mr-1" /> Timer
      </button>
      <button
        type="button"
        class="flex-1 py-2 rounded-lg text-sm font-medium transition-all"
        :class="!useTimerMode ? 'bg-emerald-500/20 text-emerald-300' : 'text-muted-foreground'"
        @click="useTimerMode = false"
      >
        Manual entry
      </button>
    </div>

    <Card class="p-6 space-y-4">
      <div>
        <label class="premium-label">Category</label>
        <select v-model="category" class="premium-select mt-2">
          <option v-for="c in categories" :key="c" :value="c">{{ c }}</option>
        </select>
      </div>
      <div>
        <label class="premium-label">Title (optional)</label>
        <input v-model="title" class="premium-input mt-2" placeholder="Morning run" />
      </div>

      <template v-if="useTimerMode">
        <div class="text-center py-4">
          <p class="text-5xl font-mono font-bold tracking-wider">{{ formatted }}</p>
          <p class="text-xs text-muted-foreground mt-2">Workout timer</p>
        </div>
        <div class="flex gap-2">
          <Button v-if="!running" variant="outline" class="flex-1" @click="start()">
            <Play class="w-4 h-4 mr-1" /> Start
          </Button>
          <Button v-else variant="outline" class="flex-1" @click="stop()">
            <Square class="w-4 h-4 mr-1" /> Pause
          </Button>
          <Button class="flex-1" :disabled="saving" @click="submitFromTimer">
            {{ saving ? 'Saving…' : 'Save workout' }}
          </Button>
        </div>
      </template>

      <template v-else>
        <div>
          <label class="premium-label">Duration (minutes)</label>
          <input v-model.number="duration" type="number" min="1" class="premium-input mt-2" />
        </div>
        <Button class="w-full" :disabled="saving" @click="submitManual">{{ saving ? 'Saving…' : 'Save workout' }}</Button>
      </template>

      <div>
        <label class="premium-label">Notes</label>
        <textarea v-model="notes" rows="3" class="premium-input mt-2 resize-none" placeholder="Optional notes…" />
      </div>
    </Card>

    <Card v-if="recentWorkouts.length" class="p-5 space-y-3">
      <div class="flex items-center justify-between">
        <h2 class="font-semibold text-sm flex items-center gap-2">
          <History class="w-4 h-4 text-emerald-400" /> Recent workouts
        </h2>
        <RouterLink to="/activities" class="text-xs text-emerald-400 hover:underline">View all</RouterLink>
      </div>
      <ul class="space-y-2">
        <li
          v-for="w in recentWorkouts"
          :key="w.id"
          class="flex justify-between text-sm rounded-lg border border-white/10 bg-white/[0.03] px-3 py-2"
        >
          <span class="truncate pr-2">{{ w.title }}</span>
          <span class="text-muted-foreground shrink-0">{{ w.durationMinutes }} min · {{ Math.round(w.caloriesBurned) }} kcal</span>
        </li>
      </ul>
    </Card>
  </div>
</template>
