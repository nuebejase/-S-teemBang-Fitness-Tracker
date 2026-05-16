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
  updateProfileApi,
} from '@/lib/api'
import { STORAGE_KEYS } from '@/constants/storage'
import type {
  Activity,
  AdminStats,
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

  const loading = ref(false)
  const bootstrapError = ref<string | null>(null)

  const unreadCount = computed(() => notifications.value.filter((n) => !n.isRead).length)

  async function refreshDashboard() {
    if (!user.value || user.value.role === 'admin') return
    dashboard.value = await fetchDashboardApi()
    goals.value = dashboard.value.activeGoals
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
    activities.value = await fetchAdminActivitiesApi()
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
    await refreshDashboard()
    await refreshTrends()
  }

  async function syncSteps(steps: number) {
    const updated = await syncStepsApi(steps)
    const idx = activities.value.findIndex(
      (a) => a.activityType === 'steps' && a.loggedAt.slice(0, 10) === updated.loggedAt.slice(0, 10),
    )
    if (idx >= 0) activities.value[idx] = updated
    else activities.value.unshift(updated)
    await refreshDashboard()
    await refreshTrends()
  }

  async function removeActivity(id: string) {
    await deleteActivityApi(id)
    activities.value = activities.value.filter((a) => a.id !== id)
    await refreshDashboard()
  }

  async function addGoal(metric: Goal['metric'], period: Goal['period'], targetValue: number) {
    const created = await createGoalApi({ metric, period, target_value: targetValue })
    goals.value.unshift(created)
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
    })
    await refreshDashboard()
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
    loading,
    bootstrapError,
    unreadCount,
    initializeApp,
    login,
    register,
    logout,
    refreshDashboard,
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
    markRead,
    markAllRead,
    addReminder,
  }
})
