<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { RouterLink } from 'vue-router'
import Avatar from '@/components/Avatar.vue'
import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import ProgressRing from '@/components/ProgressRing.vue'
import TrendChart from '@/components/TrendChart.vue'
import { usePedometer } from '@/composables/usePedometer'
import { useAppStore } from '@/stores/appStore'
import { formatNumber } from '@/lib/utils'
import type { Goal } from '@/types/domain'
import { Flame, Footprints, Target, Dumbbell, Sparkles } from 'lucide-vue-next'
import { toast } from 'vue-sonner'

const store = useAppStore()
const pedometer = usePedometer()
const stepInput = ref(0)
const syncing = ref(false)

const dash = computed(() => store.dashboard)
const profile = computed(() => store.profile)
const guest = computed(() => !store.user)

function dailyTarget(metric: Goal['metric'], profileFallback: number) {
  const goal = store.goals.find((g) => g.period === 'daily' && g.metric === metric && g.isActive)
  return goal?.targetValue ?? profileFallback
}

const stepTarget = computed(() => dailyTarget('steps', profile.value?.dailyStepTarget ?? 8000))
const calorieTarget = computed(() => dailyTarget('calories', profile.value?.dailyCalorieTarget ?? 500))
const workoutTarget = computed(() => dailyTarget('workouts', profile.value?.dailyWorkoutTarget ?? 1))

const stepProgress = computed(() =>
  dash.value ? Math.min(100, Math.round((dash.value.todaySteps / stepTarget.value) * 100)) : 0,
)

onMounted(async () => {
  if (store.user?.role === 'member') {
    await Promise.all([store.refreshProfile(), store.refreshGoals(), store.refreshDashboard()])
  }
})

watch(
  () => dash.value?.todaySteps,
  (steps) => {
    if (steps !== undefined && stepInput.value === 0) stepInput.value = steps
  },
  { immediate: true },
)

async function syncSteps() {
  if (stepInput.value <= 0) {
    toast.error('Enter a step count first')
    return
  }
  syncing.value = true
  try {
    await store.syncSteps(stepInput.value)
    toast.success('Steps synced!')
  } catch (e) {
    toast.error(e instanceof Error ? e.message : 'Sync failed')
  } finally {
    syncing.value = false
  }
}

async function togglePedometer() {
  if (pedometer.tracking.value) {
    pedometer.stop()
    stepInput.value = (dash.value?.todaySteps ?? 0) + pedometer.sessionSteps.value
    toast.info(`+${pedometer.sessionSteps.value} steps added — tap Sync to save`)
    return
  }
  pedometer.reset()
  await pedometer.start()
  toast.success('Walk simulation running — tap Stop when done')
}

watch(pedometer.sessionSteps, (n) => {
  if (pedometer.tracking.value) {
    stepInput.value = (dash.value?.todaySteps ?? 0) + n
  }
})
</script>

<template>
  <div>
    <section v-if="guest" class="relative py-20 px-4 overflow-hidden">
      <div class="absolute inset-0 bg-gradient-to-b from-emerald-500/10 via-transparent to-transparent pointer-events-none" />
      <div class="container mx-auto max-w-3xl relative text-center">
        <div class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 text-xs font-semibold uppercase tracking-wider mb-6">
          <Sparkles class="w-3.5 h-3.5" /> Premium fitness tracking
        </div>
        <h1 class="text-4xl md:text-6xl font-bold tracking-tight mb-5">
          Train smarter with
          <span class="gradient-text block mt-1">(S)TeemBang</span>
        </h1>
        <p class="text-lg text-muted-foreground mb-10 max-w-xl mx-auto">
          Track steps, log workouts, crush goals, and visualize your progress.
        </p>
        <div class="flex flex-wrap justify-center gap-3">
          <RouterLink to="/register"><Button size="lg">Get started</Button></RouterLink>
          <RouterLink to="/login"><Button size="lg" variant="outline">Sign in</Button></RouterLink>
        </div>
      </div>
    </section>

    <section v-else-if="store.user?.role === 'member'" class="container mx-auto px-4 py-8 max-w-5xl space-y-8">
      <div class="flex items-center justify-between gap-4">
        <div>
          <p class="premium-label">Welcome back</p>
          <h1 class="text-2xl md:text-3xl font-bold tracking-tight mt-1">{{ store.user.name.split(' ')[0] }} 👋</h1>
        </div>
        <RouterLink to="/profile">
          <Avatar :name="store.user.name" :src="profile?.avatarUrl" size="lg" ring />
        </RouterLink>
      </div>

      <!-- Daily goals — steps, calories, workouts -->
      <Card class="p-6 md:p-8">
        <h2 class="font-semibold mb-6">Today's daily goals</h2>
        <div class="grid grid-cols-3 gap-4 md:gap-8">
          <ProgressRing
            :value="dash?.todaySteps ?? 0"
            :max="stepTarget"
            label="Steps"
            :sublabel="`/ ${formatNumber(stepTarget)}`"
            :icon="Footprints"
            color="emerald"
            size="sm"
          />
          <ProgressRing
            :value="dash?.todayCalories ?? 0"
            :max="calorieTarget"
            label="Calories"
            :sublabel="`/ ${calorieTarget} kcal`"
            :icon="Flame"
            color="orange"
            size="sm"
          />
          <ProgressRing
            :value="dash?.todayWorkouts ?? 0"
            :max="workoutTarget"
            label="Workouts"
            :sublabel="`/ ${workoutTarget} session${workoutTarget > 1 ? 's' : ''}`"
            :icon="Dumbbell"
            color="blue"
            size="sm"
          />
        </div>
      </Card>

      <!-- Steps sync -->
      <Card class="p-6">
        <h3 class="font-semibold mb-3 flex items-center gap-2">
          <Footprints class="w-5 h-5 text-emerald-400" /> Log steps
        </h3>
        <div class="flex flex-wrap gap-2 items-center">
          <input v-model.number="stepInput" type="number" min="0" class="premium-input flex-1 min-w-[120px] max-w-[180px]" placeholder="Steps" />
          <Button variant="outline" size="sm" @click="togglePedometer">
            {{ pedometer.tracking.value ? `Stop (+${pedometer.sessionSteps.value})` : 'Simulate walk' }}
          </Button>
          <Button size="sm" :disabled="syncing" @click="syncSteps">{{ syncing ? '…' : 'Sync' }}</Button>
        </div>
        <p class="text-xs text-muted-foreground mt-2">{{ stepProgress }}% of daily step target</p>
      </Card>

      <div class="grid lg:grid-cols-2 gap-6">
        <Card class="p-6">
          <div class="flex justify-between items-center mb-5">
            <h2 class="font-semibold">14-day trend</h2>
            <RouterLink to="/analytics" class="text-xs text-emerald-400 hover:underline font-medium">Full analytics →</RouterLink>
          </div>
          <TrendChart v-if="store.trends.length" :points="store.trends" metric="steps" />
          <p v-else class="text-sm text-muted-foreground text-center py-8">Log activity to unlock trends.</p>
        </Card>

        <Card v-if="dash?.activeGoals?.length" class="p-6">
          <div class="flex justify-between items-center mb-5">
            <h2 class="font-semibold">Active goals</h2>
            <RouterLink to="/goals"><Button variant="outline" size="sm">Manage</Button></RouterLink>
          </div>
          <div class="space-y-4">
            <div v-for="g in dash.activeGoals" :key="g.id">
              <div class="flex justify-between text-sm mb-1.5">
                <span class="capitalize text-muted-foreground">{{ g.period }} {{ g.metric }}</span>
                <span class="font-medium">{{ g.progressPercent }}%</span>
              </div>
              <div class="h-2 rounded-full bg-muted overflow-hidden">
                <div class="h-full bg-gradient-to-r from-emerald-500 to-cyan-400 rounded-full transition-all" :style="{ width: `${g.progressPercent}%` }" />
              </div>
            </div>
          </div>
        </Card>
      </div>

      <div class="flex flex-wrap gap-3">
        <RouterLink to="/workouts"><Button><Dumbbell class="w-4 h-4 mr-2" /> Log workout</Button></RouterLink>
        <RouterLink to="/goals"><Button variant="outline"><Target class="w-4 h-4 mr-2" /> Goals</Button></RouterLink>
        <RouterLink to="/activities"><Button variant="outline">Activity history</Button></RouterLink>
      </div>
    </section>
  </div>
</template>
