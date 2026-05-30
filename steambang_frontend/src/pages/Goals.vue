<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import { usePedometer } from '@/composables/usePedometer'
import { useWorkoutTimer } from '@/composables/useWorkoutTimer'
import { useAppStore } from '@/stores/appStore'
import { formatNumber } from '@/lib/utils'
import type { Goal } from '@/types/domain'
import { toast } from 'vue-sonner'
import { Trash2, Footprints, Flame, Dumbbell, Timer, Play, Square } from 'lucide-vue-next'

const store = useAppStore()
const metric = ref<'steps' | 'calories' | 'workouts'>('steps')
const period = ref<'daily' | 'weekly' | 'monthly'>('daily')
const target = ref(8000)

const stepInputs = ref<Record<string, number>>({})
const calorieInputs = ref<Record<string, number>>({})
const workoutCategory = ref('running')
const activeWorkoutGoalId = ref<string | null>(null)

const pedometer = usePedometer()
const { running: timerRunning, formatted: timerFormatted, elapsedMinutes, elapsedSeconds, start: startTimer, stop: stopTimer, reset: resetTimer } = useWorkoutTimer()

const targetHints = computed(() => {
  const p = store.profile
  if (metric.value === 'steps') {
    if (period.value === 'daily') return p?.dailyStepTarget ?? 8000
    if (period.value === 'weekly') return (p?.dailyStepTarget ?? 8000) * 7
    return (p?.dailyStepTarget ?? 8000) * 30
  }
  if (metric.value === 'calories') {
    if (period.value === 'daily') return p?.dailyCalorieTarget ?? 500
    if (period.value === 'weekly') return (p?.dailyCalorieTarget ?? 500) * 7
    return (p?.dailyCalorieTarget ?? 500) * 30
  }
  if (period.value === 'daily') return p?.dailyWorkoutTarget ?? 1
  if (period.value === 'weekly') return (p?.dailyWorkoutTarget ?? 1) * 7
  return (p?.dailyWorkoutTarget ?? 1) * 30
})

watch([metric, period], () => {
  target.value = targetHints.value
})

function startWorkoutTimer(goalId: string) {
  activeWorkoutGoalId.value = goalId
  resetTimer()
  startTimer()
}

async function finishWorkoutTimer(goal: Goal) {
  if (activeWorkoutGoalId.value !== goal.id && elapsedSeconds.value === 0) {
    activeWorkoutGoalId.value = goal.id
  }
  stopTimer()
  const mins = elapsedMinutes.value
  if (elapsedSeconds.value === 0) {
    toast.error('Start the timer first')
    return
  }
  try {
    await store.logWorkout({
      category: workoutCategory.value,
      title: `${workoutCategory.value} session (${mins} min)`,
      durationMinutes: mins,
      notes: `Logged from ${goal.period} ${goal.metric} goal timer`,
    })
    toast.success(`Workout logged — ${mins} min`)
    resetTimer()
    activeWorkoutGoalId.value = null
  } catch (e) {
    toast.error(e instanceof Error ? e.message : 'Failed')
  }
}

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

async function syncStepsForGoal() {
  const steps = stepInputs.value['_global'] ?? 0
  if (steps <= 0) {
    toast.error('Enter steps first')
    return
  }
  try {
    await store.syncSteps(steps)
    toast.success('Steps logged toward your goal')
    stepInputs.value['_global'] = 0
  } catch (e) {
    toast.error(e instanceof Error ? e.message : 'Failed')
  }
}

async function toggleSimWalk() {
  if (pedometer.tracking.value) {
    pedometer.stop()
    stepInputs.value['_global'] = (stepInputs.value['_global'] ?? 0) + pedometer.sessionSteps.value
    toast.info(`+${pedometer.sessionSteps.value} steps ready — tap Log steps`)
    return
  }
  pedometer.reset()
  await pedometer.start()
  toast.success('Walk simulation running')
}

async function logCaloriesForGoal(goalId: string) {
  const cal = calorieInputs.value[goalId] ?? 0
  if (cal <= 0) {
    toast.error('Enter calories first')
    return
  }
  try {
    await store.logCalories(cal)
    toast.success(`${cal} kcal logged`)
    calorieInputs.value[goalId] = 0
  } catch (e) {
    toast.error(e instanceof Error ? e.message : 'Failed')
  }
}

function metricIcon(m: Goal['metric']) {
  if (m === 'steps') return Footprints
  if (m === 'calories') return Flame
  return Dumbbell
}

function metricColor(m: Goal['metric']) {
  if (m === 'steps') return 'from-emerald-500 to-teal-400'
  if (m === 'calories') return 'from-orange-500 to-amber-400'
  return 'from-blue-500 to-cyan-400'
}

onMounted(async () => {
  if (store.user?.role === 'member') {
    await store.refreshGoals()
  }
})
</script>

<template>
  <div class="container mx-auto px-4 py-8 max-w-2xl space-y-8">
    <div>
      <h1 class="text-2xl font-bold tracking-tight">Fitness goals</h1>
      <p class="text-muted-foreground text-sm mt-1">Each metric has its own way to track progress.</p>
    </div>

    <Card class="p-6 space-y-5">
      <h2 class="font-semibold">New goal</h2>
      <div class="grid sm:grid-cols-3 gap-4">
        <div>
          <label class="premium-label">Metric</label>
          <select v-model="metric" class="premium-select mt-2">
            <option value="steps">Steps — manual / simulate</option>
            <option value="calories">Calories — log kcal</option>
            <option value="workouts">Workouts — timer</option>
          </select>
        </div>
        <div>
          <label class="premium-label">Period</label>
          <select v-model="period" class="premium-select mt-2">
            <option value="daily">Daily</option>
            <option value="weekly">Weekly</option>
            <option value="monthly">Monthly</option>
          </select>
        </div>
        <div>
          <label class="premium-label">Target</label>
          <input v-model.number="target" type="number" min="1" class="premium-input mt-2" />
          <p class="text-[10px] text-muted-foreground mt-1">Suggested: {{ formatNumber(targetHints) }}</p>
        </div>
      </div>
      <Button @click="add">Add goal</Button>
    </Card>

    <!-- Global steps tracker -->
    <Card class="p-5 space-y-3">
      <div class="flex items-center gap-2">
        <Footprints class="w-5 h-5 text-emerald-400" />
        <h3 class="font-semibold text-sm">Track steps toward goals</h3>
      </div>
      <p class="text-xs text-muted-foreground">Enter manually or simulate a walk — then log steps.</p>
      <div class="flex flex-wrap gap-2">
        <input v-model.number="stepInputs['_global']" type="number" min="0" class="premium-input flex-1 min-w-[100px]" placeholder="Steps" />
        <Button variant="outline" size="sm" @click="toggleSimWalk">
          {{ pedometer.tracking.value ? `Stop (+${pedometer.sessionSteps})` : 'Simulate walk' }}
        </Button>
        <Button size="sm" @click="syncStepsForGoal">Log steps</Button>
      </div>
    </Card>

    <div class="space-y-4">
      <Card v-for="g in store.goals" :key="g.id" class="p-5 space-y-4">
        <div class="flex justify-between items-start gap-3">
          <div class="flex items-start gap-3 flex-1">
            <div :class="['w-10 h-10 rounded-xl flex items-center justify-center shrink-0 bg-gradient-to-br', metricColor(g.metric), 'bg-opacity-20']">
              <component :is="metricIcon(g.metric)" class="w-5 h-5 text-white" />
            </div>
            <div class="flex-1 min-w-0">
              <p class="font-semibold capitalize">{{ g.period }} {{ g.metric }}</p>
              <p class="text-sm text-muted-foreground">
                {{ formatNumber(g.currentValue) }} / {{ formatNumber(g.targetValue) }}
                <span v-if="g.metric === 'calories'"> kcal</span>
                <span v-else-if="g.metric === 'workouts'"> sessions</span>
              </p>
              <div class="mt-2 h-2 w-full rounded-full bg-muted overflow-hidden">
                <div :class="['h-full rounded-full bg-gradient-to-r transition-all', metricColor(g.metric)]" :style="{ width: `${g.progressPercent}%` }" />
              </div>
              <p class="text-xs text-muted-foreground mt-1">{{ g.progressPercent }}% complete</p>
            </div>
          </div>
          <Button variant="ghost" size="icon" @click="remove(g.id)"><Trash2 class="w-4 h-4 text-red-400" /></Button>
        </div>

        <!-- Workout timer tracker -->
        <div v-if="g.metric === 'workouts'" class="rounded-xl border border-white/10 bg-white/[0.03] p-4 space-y-3">
          <div class="flex items-center gap-2 text-sm font-medium">
            <Timer class="w-4 h-4 text-blue-400" /> Workout timer
          </div>
          <select v-model="workoutCategory" class="premium-select text-sm">
            <option value="running">Running</option>
            <option value="walking">Walking</option>
            <option value="cycling">Cycling</option>
            <option value="strength">Strength</option>
            <option value="yoga">Yoga</option>
            <option value="hiit">HIIT</option>
            <option value="swimming">Swimming</option>
            <option value="other">Other</option>
          </select>
          <p class="text-3xl font-mono font-bold text-center tracking-wider">
            {{ activeWorkoutGoalId === g.id || !activeWorkoutGoalId ? timerFormatted : '00:00' }}
          </p>
          <div class="flex gap-2">
            <Button
              v-if="!timerRunning || activeWorkoutGoalId !== g.id"
              variant="outline"
              class="flex-1"
              @click="startWorkoutTimer(g.id)"
            >
              <Play class="w-4 h-4 mr-1" /> Start
            </Button>
            <Button v-else variant="outline" class="flex-1" @click="stopTimer()">
              <Square class="w-4 h-4 mr-1" /> Pause
            </Button>
            <Button class="flex-1" @click="finishWorkoutTimer(g)">Log workout</Button>
          </div>
        </div>

        <!-- Calorie tracker -->
        <div v-else-if="g.metric === 'calories'" class="rounded-xl border border-white/10 bg-white/[0.03] p-4 space-y-3">
          <div class="flex items-center gap-2 text-sm font-medium">
            <Flame class="w-4 h-4 text-orange-400" /> Log calories burned
          </div>
          <div class="flex gap-2">
            <input v-model.number="calorieInputs[g.id]" type="number" min="1" class="premium-input flex-1" placeholder="e.g. 250 kcal" />
            <Button @click="logCaloriesForGoal(g.id)">Log kcal</Button>
          </div>
          <p class="text-xs text-muted-foreground">Also counts calories from logged workouts automatically.</p>
        </div>

        <!-- Steps hint -->
        <div v-else class="rounded-xl border border-white/10 bg-white/[0.03] p-3">
          <p class="text-xs text-muted-foreground">
            <Footprints class="w-3.5 h-3.5 inline text-emerald-400 mr-1" />
            Use the steps tracker above to log progress toward this goal.
          </p>
        </div>
      </Card>
    </div>
  </div>
</template>
