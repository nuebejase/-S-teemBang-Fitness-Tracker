import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import {
  createActivityApi,
  createGoalApi,
  createReminderApi,
  deleteActivityApi,
  deleteGoalApi,
  fetchActivitiesApi,
  fetchAdminActivitiesApi,
  fetchAdminStatsApi,
  fetchAdminUsersApi,
  fetchDashboardApi,
  fetchGoalsApi,
  fetchMeApi,
  fetchNotificationsApi,
  fetchProfileApi,
  fetchTrendsApi,
  loginApi,
  markAllNotificationsReadApi,
  markNotificationReadApi,
  registerApi,
  syncStepsApi,
  updateGoalApi,
  updateProfileApi,
  uploadAvatarApi,
} from '@/lib/api'
import { STORAGE_KEYS } from '@/constants/storage'
import type {
  Activity,
  AdminStats,
  AdminUser,
  Dashboard,
  Goal,
  Notification,
  Profile,
  TrendPoint,
  User,
} from '@/types/domain'

export const useAppStore = defineStore('app', () => {
  const user = ref<User | null>(null)
  const profile = ref<Profile | null>(null)
  const dashboard = ref<Dashboard | null>(null)
  const activities = ref<Activity[]>([])
  const goals = ref<Goal[]>([])
  const trends = ref<TrendPoint[]>([])
  const notifications = ref<Notification[]>([])
  const adminStats = ref<AdminStats | null>(null)
  const adminUsers = ref<AdminUser[]>([])

  const loading = ref(false)
  const bootstrapError = ref<string | null>(null)

  const unreadCount = computed(() => notifications.value.filter((n) => !n.isRead).length)

  async function refreshDashboard() {
    if (!user.value || user.value.role === 'admin') return
    dashboard.value = await fetchDashboardApi()
  }

  async function refreshGoals() {
    if (!user.value || user.value.role === 'admin') return
    goals.value = await fetchGoalsApi()
  }

  async function refreshAfterActivity() {
    if (!user.value || user.value.role === 'admin') return
    await Promise.all([
      refreshDashboard(),
      refreshGoals(),
      refreshNotifications(),
      refreshTrends(),
      refreshActivities(),
    ])
  }

  async function syncDailyGoalsFromProfile() {
    if (!profile.value) return
    const allGoals = await fetchGoalsApi()
    const pairs: { metric: Goal['metric']; target: number }[] = [
      { metric: 'steps', target: profile.value.dailyStepTarget },
      { metric: 'calories', target: profile.value.dailyCalorieTarget },
      { metric: 'workouts', target: profile.value.dailyWorkoutTarget },
    ]
    for (const { metric, target } of pairs) {
      const existing = allGoals.find((g) => g.metric === metric && g.period === 'daily' && g.isActive)
      if (existing) {
        if (existing.targetValue !== target) {
          await updateGoalApi(existing.id, { target_value: target })
        }
      } else {
        await createGoalApi({ metric, period: 'daily', target_value: target })
      }
    }
    await refreshGoals()
  }

  async function syncProfileTargetFromDailyGoal(metric: Goal['metric'], targetValue: number) {
    if (!profile.value) return
    const patch: Parameters<typeof updateProfileApi>[0] = {}
    if (metric === 'steps') patch.daily_step_target = targetValue
    if (metric === 'calories') patch.daily_calorie_target = targetValue
    if (metric === 'workouts') patch.daily_workout_target = targetValue
    profile.value = await updateProfileApi(patch)
  }

  async function refreshActivities() {
    if (!user.value) return
    if (user.value.role === 'admin') {
      activities.value = await fetchAdminActivitiesApi()
    } else {
      activities.value = await fetchActivitiesApi()
    }
  }

  async function refreshTrends(days = 14) {
    if (!user.value || user.value.role === 'admin') return
    trends.value = await fetchTrendsApi(days)
  }

  async function refreshNotifications() {
    if (!user.value || user.value.role === 'admin') return
    notifications.value = await fetchNotificationsApi()
  }

  async function refreshProfile() {
    if (!user.value || user.value.role === 'admin') return
    profile.value = await fetchProfileApi()
  }

  async function refreshAdmin() {
    if (user.value?.role !== 'admin') return
    adminStats.value = await fetchAdminStatsApi()
    adminUsers.value = await fetchAdminUsersApi()
    activities.value = adminUsers.value.flatMap((u) => u.recentActivities)
  }

  async function initializeApp() {
    loading.value = true
    bootstrapError.value = null
    try {
      const token = localStorage.getItem(STORAGE_KEYS.accessToken)
      if (!token) {
        user.value = null
        return
      }
      user.value = await fetchMeApi()
      if (user.value.role === 'admin') {
        await refreshAdmin()
      } else {
        await Promise.all([
          refreshProfile(),
          refreshDashboard(),
          refreshActivities(),
          refreshTrends(),
          refreshNotifications(),
        ])
        const allGoals = await fetchGoalsApi()
        goals.value = allGoals
      }
    } catch (e) {
      localStorage.removeItem(STORAGE_KEYS.accessToken)
      user.value = null
      bootstrapError.value = e instanceof Error ? e.message : 'Could not connect to API'
    } finally {
      loading.value = false
    }
  }

  async function login(email: string, password: string) {
    const token = await loginApi(email, password)
    localStorage.setItem(STORAGE_KEYS.accessToken, token)
    await initializeApp()
  }

  async function register(name: string, email: string, password: string) {
    const token = await registerApi(name, email, password)
    localStorage.setItem(STORAGE_KEYS.accessToken, token)
    await initializeApp()
  }

  function logout() {
    user.value = null
    profile.value = null
    dashboard.value = null
    activities.value = []
    goals.value = []
    trends.value = []
    notifications.value = []
    adminStats.value = null
    adminUsers.value = []
    localStorage.removeItem(STORAGE_KEYS.accessToken)
  }

  async function logWorkout(payload: {
    category: string
    title: string
    durationMinutes: number
    notes?: string
  }) {
    const created = await createActivityApi({
      activity_type: 'workout',
      category: payload.category,
      title: payload.title,
      duration_minutes: payload.durationMinutes,
      notes: payload.notes ?? '',
    })
    activities.value.unshift(created)
    await refreshAfterActivity()
    return created
  }

  async function syncSteps(steps: number) {
    const updated = await syncStepsApi(steps)
    const idx = activities.value.findIndex(
      (a) => a.activityType === 'steps' && a.loggedAt.slice(0, 10) === updated.loggedAt.slice(0, 10),
    )
    if (idx >= 0) activities.value[idx] = updated
    else activities.value.unshift(updated)
    await refreshAfterActivity()
  }

  async function removeActivity(id: string) {
    await deleteActivityApi(id)
    activities.value = activities.value.filter((a) => a.id !== id)
    await refreshAfterActivity()
  }

  async function addGoal(metric: Goal['metric'], period: Goal['period'], targetValue: number) {
    const created = await createGoalApi({ metric, period, target_value: targetValue })
    goals.value.unshift(created)
    if (period === 'daily') {
      await syncProfileTargetFromDailyGoal(metric, targetValue)
    }
    await refreshDashboard()
  }

  async function removeGoal(id: string) {
    await deleteGoalApi(id)
    goals.value = goals.value.filter((g) => g.id !== id)
    await refreshDashboard()
  }

  async function saveProfile(payload: Partial<Profile>) {
    profile.value = await updateProfileApi({
      height_cm: payload.heightCm ?? undefined,
      weight_kg: payload.weightKg ?? undefined,
      age: payload.age ?? undefined,
      fitness_level: payload.fitnessLevel,
      daily_step_target: payload.dailyStepTarget,
      daily_calorie_target: payload.dailyCalorieTarget,
      daily_workout_target: payload.dailyWorkoutTarget,
    })
    await syncDailyGoalsFromProfile()
    await refreshDashboard()
  }

  async function logCalories(calories: number) {
    const created = await createActivityApi({
      activity_type: 'workout',
      category: 'other',
      title: 'Calorie log',
      duration_minutes: 1,
      calories_burned: calories,
    })
    activities.value.unshift(created)
    await refreshAfterActivity()
    return created
  }

  async function uploadAvatar(file: File) {
    profile.value = await uploadAvatarApi(file)
  }

  async function markRead(id: string) {
    const updated = await markNotificationReadApi(id)
    const idx = notifications.value.findIndex((n) => n.id === id)
    if (idx >= 0) notifications.value[idx] = updated
  }

  async function markAllRead() {
    await markAllNotificationsReadApi()
    notifications.value = notifications.value.map((n) => ({ ...n, isRead: true }))
  }

  async function addReminder(title: string, body: string) {
    const n = await createReminderApi(title, body)
    notifications.value.unshift(n)
  }

  return {
    user,
    profile,
    dashboard,
    activities,
    goals,
    trends,
    notifications,
    adminStats,
    adminUsers,
    loading,
    bootstrapError,
    unreadCount,
    initializeApp,
    login,
    register,
    logout,
    refreshDashboard,
    refreshGoals,
    refreshAfterActivity,
    refreshActivities,
    refreshTrends,
    refreshNotifications,
    refreshProfile,
    refreshAdmin,
    logWorkout,
    syncSteps,
    removeActivity,
    addGoal,
    removeGoal,
    saveProfile,
    uploadAvatar,
    logCalories,
    markRead,
    markAllRead,
    addReminder,
  }
})
