<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import Avatar from '@/components/Avatar.vue'
import Card from '@/components/ui/Card.vue'
import ProgressRing from '@/components/ProgressRing.vue'
import StatCard from '@/components/StatCard.vue'
import { useAppStore } from '@/stores/appStore'
import { formatDateTime, formatNumber } from '@/lib/utils'
import type { AdminUser } from '@/types/domain'
import {
  Activity,
  ChevronDown,
  ChevronUp,
  Flame,
  Footprints,
  Shield,
  Target,
  UserCheck,
  Users,
  Dumbbell,
  CheckCircle2,
  AlertCircle,
} from 'lucide-vue-next'

const store = useAppStore()
const expandedUserId = ref<string | null>(null)

onMounted(() => store.refreshAdmin())

const members = computed(() => store.adminUsers.filter((u) => u.role === 'member'))
const admins = computed(() => store.adminUsers.filter((u) => u.role === 'admin'))
const stats = computed(() => store.adminStats)

const platformFeed = computed(() =>
  members.value
    .flatMap((u) =>
      u.recentActivities.map((a) => ({
        ...a,
        userName: u.name,
        userAvatar: u.avatarUrl,
      })),
    )
    .sort((a, b) => b.loggedAt.localeCompare(a.loggedAt))
    .slice(0, 12),
)

function toggleUser(u: AdminUser) {
  expandedUserId.value = expandedUserId.value === u.id ? null : u.id
}

function activityIcon(type: string) {
  return type === 'workout' ? Dumbbell : Footprints
}

function pct(current: number, target: number) {
  return target > 0 ? Math.min(100, Math.round((current / target) * 100)) : 0
}

function goalBarColor(metric: string) {
  if (metric === 'calories') return 'from-orange-500 to-amber-400'
  if (metric === 'workouts') return 'from-blue-500 to-cyan-400'
  return 'from-emerald-500 to-teal-400'
}
</script>

<template>
  <div class="container mx-auto px-4 py-8 max-w-5xl space-y-8">
    <div class="flex items-center gap-4">
      <div class="w-14 h-14 rounded-2xl bg-gradient-to-br from-violet-500 to-fuchsia-600 flex items-center justify-center shadow-lg shadow-violet-500/25">
        <Shield class="w-7 h-7 text-white" />
      </div>
      <div>
        <h1 class="text-3xl font-bold tracking-tight gradient-text-admin">Admin Console</h1>
        <p class="text-muted-foreground text-sm mt-0.5">Monitor members, daily goals, and platform activity</p>
      </div>
    </div>

    <!-- Platform stats -->
    <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <StatCard label="Total users" :value="String(stats?.totalUsers ?? 0)" :icon="Users" accent="bg-violet-500/15 text-violet-300 border border-violet-500/20" glow="rgba(139,92,246,0.3)" />
      <StatCard label="Activities logged" :value="String(stats?.totalActivities ?? 0)" :icon="Activity" accent="bg-cyan-500/15 text-cyan-300 border border-cyan-500/20" />
      <StatCard label="Goals set" :value="String(stats?.totalGoals ?? 0)" :icon="Target" accent="bg-fuchsia-500/15 text-fuchsia-300 border border-fuchsia-500/20" />
      <StatCard label="Active (7d)" :value="String(stats?.activeMembers ?? 0)" :icon="UserCheck" accent="bg-emerald-500/15 text-emerald-300 border border-emerald-500/20" />
    </div>

    <!-- Platform today — mirrors member home daily goals -->
    <Card class="p-6 md:p-8">
      <div class="flex flex-wrap justify-between items-start gap-3 mb-6">
        <div>
          <h2 class="font-semibold">Platform activity today</h2>
          <p class="text-xs text-muted-foreground mt-1">Combined totals across all members</p>
        </div>
        <div class="flex items-center gap-2 text-xs text-muted-foreground">
          <CheckCircle2 class="w-4 h-4 text-emerald-400" />
          {{ stats?.profilesComplete ?? 0 }} complete profiles
        </div>
      </div>
      <div class="grid grid-cols-3 gap-4 md:gap-8">
        <ProgressRing
          :value="stats?.todayPlatformSteps ?? 0"
          :max="Math.max(stats?.todayPlatformSteps ?? 1, 1)"
          label="Steps"
          sublabel="today"
          :icon="Footprints"
          color="emerald"
          size="sm"
        />
        <ProgressRing
          :value="stats?.todayPlatformCalories ?? 0"
          :max="Math.max(stats?.todayPlatformCalories ?? 1, 1)"
          label="Calories"
          sublabel="kcal today"
          :icon="Flame"
          color="orange"
          size="sm"
        />
        <ProgressRing
          :value="stats?.todayPlatformWorkouts ?? 0"
          :max="Math.max(stats?.todayPlatformWorkouts ?? 1, 1)"
          label="Workouts"
          sublabel="sessions today"
          :icon="Dumbbell"
          color="blue"
          size="sm"
        />
      </div>
    </Card>

    <!-- Members -->
    <section>
      <h2 class="text-lg font-semibold mb-4 flex items-center gap-2">
        <Users class="w-5 h-5 text-violet-400" />
        Members
        <span class="text-sm font-normal text-muted-foreground">({{ members.length }})</span>
      </h2>
      <div class="space-y-3">
        <Card
          v-for="u in members"
          :key="u.id"
          class="overflow-hidden transition-all"
          :class="expandedUserId === u.id ? 'border-violet-500/30' : ''"
        >
          <button
            type="button"
            class="w-full p-5 text-left hover:bg-white/[0.02] transition-colors"
            @click="toggleUser(u)"
          >
            <div class="flex items-start gap-4">
              <Avatar :name="u.name" :src="u.avatarUrl" size="md" ring />
              <div class="flex-1 min-w-0">
                <div class="flex flex-wrap items-center gap-2">
                  <p class="font-semibold truncate">{{ u.name }}</p>
                  <span
                    v-if="u.profileComplete"
                    class="text-[10px] uppercase tracking-wider px-2 py-0.5 rounded-full bg-emerald-500/15 text-emerald-300 border border-emerald-500/20"
                  >
                    Profile complete
                  </span>
                  <span
                    v-else
                    class="text-[10px] uppercase tracking-wider px-2 py-0.5 rounded-full bg-amber-500/15 text-amber-300 border border-amber-500/20 flex items-center gap-1"
                  >
                    <AlertCircle class="w-3 h-3" /> Setup pending
                  </span>
                </div>
                <p class="text-sm text-muted-foreground truncate">{{ u.email }}</p>
                <p v-if="u.fitnessLevel" class="text-xs text-muted-foreground capitalize mt-0.5">{{ u.fitnessLevel }} · {{ u.streakDays }}d streak</p>

                <!-- Daily progress mini bars (like member home) -->
                <div class="grid grid-cols-3 gap-2 mt-3">
                  <div>
                    <div class="flex justify-between text-[10px] text-muted-foreground mb-1">
                      <Footprints class="w-3 h-3 text-emerald-400" />
                      <span>{{ pct(u.todaySteps, u.dailyStepTarget) }}%</span>
                    </div>
                    <div class="h-1.5 rounded-full bg-muted overflow-hidden">
                      <div class="h-full bg-emerald-500 rounded-full" :style="{ width: `${pct(u.todaySteps, u.dailyStepTarget)}%` }" />
                    </div>
                    <p class="text-[10px] text-muted-foreground mt-0.5">{{ formatNumber(u.todaySteps) }}/{{ formatNumber(u.dailyStepTarget) }}</p>
                  </div>
                  <div>
                    <div class="flex justify-between text-[10px] text-muted-foreground mb-1">
                      <Flame class="w-3 h-3 text-orange-400" />
                      <span>{{ pct(u.todayCalories, u.dailyCalorieTarget) }}%</span>
                    </div>
                    <div class="h-1.5 rounded-full bg-muted overflow-hidden">
                      <div class="h-full bg-orange-500 rounded-full" :style="{ width: `${pct(u.todayCalories, u.dailyCalorieTarget)}%` }" />
                    </div>
                    <p class="text-[10px] text-muted-foreground mt-0.5">{{ u.todayCalories }}/{{ u.dailyCalorieTarget }} kcal</p>
                  </div>
                  <div>
                    <div class="flex justify-between text-[10px] text-muted-foreground mb-1">
                      <Dumbbell class="w-3 h-3 text-blue-400" />
                      <span>{{ pct(u.todayWorkouts, u.dailyWorkoutTarget) }}%</span>
                    </div>
                    <div class="h-1.5 rounded-full bg-muted overflow-hidden">
                      <div class="h-full bg-blue-500 rounded-full" :style="{ width: `${pct(u.todayWorkouts, u.dailyWorkoutTarget)}%` }" />
                    </div>
                    <p class="text-[10px] text-muted-foreground mt-0.5">{{ u.todayWorkouts }}/{{ u.dailyWorkoutTarget }} workouts</p>
                  </div>
                </div>
              </div>
              <component :is="expandedUserId === u.id ? ChevronUp : ChevronDown" class="w-5 h-5 text-muted-foreground shrink-0 mt-1" />
            </div>
          </button>

          <div v-if="expandedUserId === u.id" class="border-t border-white/[0.06] px-5 pb-5 pt-4 space-y-5">
            <!-- Daily targets from profile -->
            <div>
              <p class="premium-label mb-3">Daily targets (from profile)</p>
              <div class="grid sm:grid-cols-3 gap-2 text-sm">
                <div class="rounded-xl bg-white/[0.03] border border-white/[0.06] p-3">
                  <Footprints class="w-4 h-4 text-emerald-400 mb-1" />
                  <p class="text-xs text-muted-foreground">Steps</p>
                  <p class="font-semibold">{{ formatNumber(u.dailyStepTarget) }}</p>
                </div>
                <div class="rounded-xl bg-white/[0.03] border border-white/[0.06] p-3">
                  <Flame class="w-4 h-4 text-orange-400 mb-1" />
                  <p class="text-xs text-muted-foreground">Calories</p>
                  <p class="font-semibold">{{ u.dailyCalorieTarget }} kcal</p>
                </div>
                <div class="rounded-xl bg-white/[0.03] border border-white/[0.06] p-3">
                  <Dumbbell class="w-4 h-4 text-blue-400 mb-1" />
                  <p class="text-xs text-muted-foreground">Workouts</p>
                  <p class="font-semibold">{{ u.dailyWorkoutTarget }} session{{ u.dailyWorkoutTarget > 1 ? 's' : '' }}</p>
                </div>
              </div>
            </div>

            <!-- Active goals -->
            <div v-if="u.activeGoals.length">
              <p class="premium-label mb-3">Active goals</p>
              <div class="space-y-2">
                <div v-for="g in u.activeGoals" :key="g.id" class="rounded-xl bg-white/[0.03] border border-white/[0.06] p-3">
                  <div class="flex justify-between text-sm mb-1.5">
                    <span class="capitalize">{{ g.period }} {{ g.metric }}</span>
                    <span class="font-medium">{{ g.progressPercent }}%</span>
                  </div>
                  <div class="h-1.5 rounded-full bg-muted overflow-hidden">
                    <div :class="['h-full rounded-full bg-gradient-to-r', goalBarColor(g.metric)]" :style="{ width: `${g.progressPercent}%` }" />
                  </div>
                  <p class="text-xs text-muted-foreground mt-1">
                    {{ formatNumber(g.currentValue) }} / {{ formatNumber(g.targetValue) }}
                    <span v-if="g.metric === 'calories'"> kcal</span>
                    <span v-else-if="g.metric === 'workouts'"> sessions</span>
                  </p>
                </div>
              </div>
            </div>

            <!-- Recent activity -->
            <div>
              <p class="premium-label mb-3">Recent activity</p>
              <div v-if="u.recentActivities.length" class="space-y-2">
                <div
                  v-for="a in u.recentActivities"
                  :key="a.id"
                  class="flex items-center gap-3 p-3 rounded-xl bg-white/[0.03] border border-white/[0.05]"
                >
                  <div
                    class="w-9 h-9 rounded-xl flex items-center justify-center shrink-0"
                    :class="a.activityType === 'workout' ? 'bg-violet-500/15 text-violet-300' : 'bg-emerald-500/15 text-emerald-300'"
                  >
                    <component :is="activityIcon(a.activityType)" class="w-4 h-4" />
                  </div>
                  <div class="flex-1 min-w-0">
                    <p class="text-sm font-medium truncate">{{ a.title }}</p>
                    <p class="text-xs text-muted-foreground capitalize">
                      {{ a.activityType }} · {{ a.category }}
                      <span v-if="a.steps"> · {{ a.steps.toLocaleString() }} steps</span>
                      <span v-if="a.durationMinutes"> · {{ a.durationMinutes }} min</span>
                      · {{ a.caloriesBurned }} kcal
                    </p>
                  </div>
                  <span class="text-xs text-muted-foreground shrink-0">{{ formatDateTime(a.loggedAt) }}</span>
                </div>
              </div>
              <p v-else class="text-sm text-muted-foreground py-4 text-center">No activity logged yet.</p>
            </div>
          </div>
        </Card>
        <p v-if="!members.length" class="text-muted-foreground text-sm text-center py-8">No members registered yet.</p>
      </div>
    </section>

    <!-- Platform activity feed -->
    <section v-if="platformFeed.length">
      <h2 class="text-lg font-semibold mb-4 flex items-center gap-2">
        <Activity class="w-5 h-5 text-cyan-400" />
        Latest platform activity
      </h2>
      <Card class="divide-y divide-white/[0.06]">
        <div v-for="a in platformFeed" :key="`${a.userName}-${a.id}`" class="p-4 flex items-center gap-3">
          <Avatar :name="a.userName" :src="a.userAvatar" size="sm" />
          <div class="flex-1 min-w-0">
            <p class="text-sm">
              <span class="font-medium">{{ a.userName }}</span>
              <span class="text-muted-foreground"> · {{ a.title }}</span>
            </p>
            <p class="text-xs text-muted-foreground capitalize">
              {{ a.activityType }}
              <span v-if="a.steps"> · {{ a.steps.toLocaleString() }} steps</span>
              <span v-if="a.durationMinutes"> · {{ a.durationMinutes }} min timer</span>
              · {{ a.caloriesBurned }} kcal
            </p>
          </div>
          <span class="text-xs text-muted-foreground shrink-0">{{ formatDateTime(a.loggedAt) }}</span>
        </div>
      </Card>
    </section>

    <section v-if="admins.length">
      <h2 class="text-lg font-semibold mb-4">Administrators</h2>
      <div class="grid sm:grid-cols-2 gap-3">
        <Card v-for="u in admins" :key="u.id" class="p-4 flex items-center gap-3">
          <Avatar :name="u.name" :src="u.avatarUrl" size="sm" />
          <div>
            <p class="font-medium">{{ u.name }}</p>
            <p class="text-xs text-muted-foreground">{{ u.email }}</p>
          </div>
        </Card>
      </div>
    </section>
  </div>
</template>
