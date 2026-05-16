<script setup lang="ts">
import { computed, ref } from 'vue'
import { RouterLink } from 'vue-router'
import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import StatCard from '@/components/StatCard.vue'
import TrendChart from '@/components/TrendChart.vue'
import { useAppStore } from '@/stores/appStore'
import { formatNumber } from '@/lib/utils'
import { Activity, Flame, Footprints, Target, TrendingUp, Dumbbell } from 'lucide-vue-next'
import { toast } from 'vue-sonner'

const store = useAppStore()
const stepInput = ref(0)
const syncing = ref(false)

const dash = computed(() => store.dashboard)
const profile = computed(() => store.profile)
const guest = computed(() => !store.user)
const stepTarget = computed(() => profile.value?.dailyStepTarget ?? 8000)
const stepProgress = computed(() => {
  if (!dash.value) return 0
  return Math.min(100, Math.round((dash.value.todaySteps / stepTarget.value) * 100))
})

async function syncSteps() {
  if (stepInput.value <= 0) {
    toast.error('Enter a step count first')
    return
  }
  syncing.value = true
  try {
    await store.syncSteps(stepInput.value)
    toast.success('Steps synced!')
    await store.refreshDashboard()
  } catch (e) {
    toast.error(e instanceof Error ? e.message : 'Sync failed')
  } finally {
    syncing.value = false
  }
}

function useDeviceSteps() {
  if (typeof window !== 'undefined' && 'DeviceMotionEvent' in window) {
    stepInput.value = Math.min(12000, (dash.value?.todaySteps ?? 0) + Math.floor(Math.random() * 800) + 200)
    toast.info('Simulated pedometer reading — tap Sync to save')
  } else {
    toast.info('Device motion unavailable in this browser; enter steps manually')
  }
}
</script>

<template>
  <div>
    <section class="bg-gradient-to-br from-emerald-50 via-teal-50 to-cyan-50 py-14">
      <div class="container mx-auto px-4">
        <div class="max-w-3xl">
          <p class="text-emerald-700 font-semibold text-sm uppercase tracking-wide mb-2">Fitness Tracking</p>
          <h1 class="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            Move smarter with
            <span class="text-emerald-600">(S)TeemBang</span>
          </h1>
          <p class="text-lg text-gray-600 mb-8">
            Track steps, log workouts, set measurable goals, and visualize your progress — built for health-conscious
            students and professionals.
          </p>
          <div v-if="guest" class="flex flex-wrap gap-3">
            <RouterLink to="/register"><Button size="lg">Get started free</Button></RouterLink>
            <RouterLink to="/login"><Button size="lg" variant="outline">Sign in</Button></RouterLink>
            <RouterLink to="/about"><Button size="lg" variant="ghost">About the project</Button></RouterLink>
          </div>
        </div>
      </div>
    </section>

    <section v-if="guest" class="container mx-auto px-4 py-12 grid md:grid-cols-3 gap-6">
      <Card class="p-6">
        <Footprints class="w-8 h-8 text-emerald-600 mb-3" />
        <h3 class="font-semibold text-lg mb-2">Activity tracking</h3>
        <p class="text-muted-foreground text-sm">Log steps and workouts with automatic calorie estimates.</p>
      </Card>
      <Card class="p-6">
        <Target class="w-8 h-8 text-emerald-600 mb-3" />
        <h3 class="font-semibold text-lg mb-2">Goal setting</h3>
        <p class="text-muted-foreground text-sm">Daily, weekly, and monthly targets you can actually hit.</p>
      </Card>
      <Card class="p-6">
        <TrendingUp class="w-8 h-8 text-emerald-600 mb-3" />
        <h3 class="font-semibold text-lg mb-2">Analytics dashboard</h3>
        <p class="text-muted-foreground text-sm">Charts and trends for long-term engagement.</p>
      </Card>
    </section>

    <section v-else-if="store.user?.role === 'member'" class="container mx-auto px-4 py-8 space-y-8">
      <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          label="Today's steps"
          :value="formatNumber(dash?.todaySteps ?? 0)"
          :sub="`${stepProgress}% of ${formatNumber(stepTarget)} goal`"
          :icon="Footprints"
        />
        <StatCard
          label="Calories burned"
          :value="String(dash?.todayCalories ?? 0)"
          sub="Today"
          :icon="Flame"
          accent="bg-orange-100 text-orange-600"
        />
        <StatCard
          label="Workouts"
          :value="String(dash?.todayWorkouts ?? 0)"
          sub="Today"
          :icon="Dumbbell"
          accent="bg-blue-100 text-blue-600"
        />
        <StatCard
          label="Streak"
          :value="`${dash?.streakDays ?? 0} days`"
          sub="Keep it going!"
          :icon="Activity"
          accent="bg-violet-100 text-violet-600"
        />
      </div>

      <div class="grid lg:grid-cols-2 gap-6">
        <Card class="p-6">
          <h2 class="font-semibold text-lg mb-4 flex items-center gap-2">
            <Footprints class="w-5 h-5 text-emerald-600" /> Sync steps (pedometer)
          </h2>
          <p class="text-sm text-muted-foreground mb-4">
            Update today's step count from your device or enter manually.
          </p>
          <div class="flex flex-wrap gap-3 items-end">
            <div class="flex-1 min-w-[140px]">
              <label class="text-xs font-medium text-muted-foreground">Steps</label>
              <input
                v-model.number="stepInput"
                type="number"
                min="0"
                class="mt-1 w-full px-3 py-2 rounded-lg border bg-background"
                placeholder="e.g. 6500"
              />
            </div>
            <Button variant="outline" @click="useDeviceSteps">Read device</Button>
            <Button :disabled="syncing" @click="syncSteps">{{ syncing ? 'Syncing…' : 'Sync' }}</Button>
          </div>
          <div class="mt-4 h-2 rounded-full bg-muted overflow-hidden">
            <div class="h-full bg-emerald-500 transition-all" :style="{ width: `${stepProgress}%` }" />
          </div>
        </Card>

        <Card class="p-6">
          <div class="flex justify-between items-center mb-4">
            <h2 class="font-semibold text-lg">14-day steps</h2>
            <RouterLink to="/analytics" class="text-sm text-emerald-600 hover:underline">View all</RouterLink>
          </div>
          <TrendChart v-if="store.trends.length" :points="store.trends" metric="steps" />
          <p v-else class="text-sm text-muted-foreground">Log activity to see trends.</p>
        </Card>
      </div>

      <Card v-if="dash?.activeGoals?.length" class="p-6">
        <div class="flex justify-between items-center mb-4">
          <h2 class="font-semibold text-lg">Active goals</h2>
          <RouterLink to="/goals"><Button variant="outline" size="sm">Manage</Button></RouterLink>
        </div>
        <div class="grid md:grid-cols-3 gap-4">
          <div v-for="g in dash.activeGoals" :key="g.id" class="rounded-lg border p-4">
            <p class="text-sm text-muted-foreground capitalize">{{ g.period }} {{ g.metric }}</p>
            <p class="font-bold mt-1">{{ formatNumber(g.currentValue) }} / {{ formatNumber(g.targetValue) }}</p>
            <div class="mt-2 h-2 rounded-full bg-muted overflow-hidden">
              <div class="h-full bg-emerald-500" :style="{ width: `${g.progressPercent}%` }" />
            </div>
            <p class="text-xs text-muted-foreground mt-1">{{ g.progressPercent }}% complete</p>
          </div>
        </div>
      </Card>

      <div class="flex flex-wrap gap-3">
        <RouterLink to="/workouts"><Button><Dumbbell class="w-4 h-4 mr-2" /> Log workout</Button></RouterLink>
        <RouterLink to="/activities"><Button variant="outline">Activity history</Button></RouterLink>
      </div>
    </section>
  </div>
</template>
