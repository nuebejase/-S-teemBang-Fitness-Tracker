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

function resolveApiBase(): string {
  const raw = import.meta.env.VITE_API_URL as string | undefined
  if (typeof raw === 'string' && raw.trim() !== '') {
    return raw.replace(/\/$/, '')
  }
  if (import.meta.env.DEV) return ''
  return 'http://localhost:8000'
}

const API_BASE = resolveApiBase()

type ApiDetail = string | { msg?: string }[] | Record<string, unknown>

function formatError(res: Response, data: unknown): string {
  const d = data as { detail?: ApiDetail }
  const detail = d?.detail
  if (typeof detail === 'string') return detail
  if (Array.isArray(detail)) {
    return detail
      .map((x) =>
        typeof x === 'object' && x && 'msg' in x ? String((x as { msg: string }).msg) : JSON.stringify(x),
      )
      .join(', ')
  }
  if (detail && typeof detail === 'object') return JSON.stringify(detail)
  return res.statusText || 'Request failed'
}

export async function apiJson<T>(path: string, init?: RequestInit): Promise<T> {
  const url = `${API_BASE}${path.startsWith('/') ? path : `/${path}`}`
  const headers = new Headers(init?.headers)
  const hasBody = init?.body !== undefined && init?.body !== null
  if (hasBody && !headers.has('Content-Type')) {
    headers.set('Content-Type', 'application/json')
  }
  const token = localStorage.getItem(STORAGE_KEYS.accessToken)
  if (token) headers.set('Authorization', `Bearer ${token}`)

  let res: Response
  try {
    res = await fetch(url, { ...init, headers })
  } catch (e) {
    const hint =
      import.meta.env.DEV && API_BASE === ''
        ? ' Start the API: cd steambang_backend && .venv\\Scripts\\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000'
        : ` (${url})`
    throw new Error(e instanceof TypeError ? `Cannot reach (S)TeemBang API.${hint}` : String(e))
  }

  const text = await res.text()
  const data = text ? (JSON.parse(text) as unknown) : null
  if (!res.ok) throw new Error(formatError(res, data))
  if (res.status === 204) return undefined as T
  return data as T
}

/* --- mappers --- */

function mapProfile(p: {
  height_cm: number | null
  weight_kg: number | null
  age: number | null
  fitness_level: string
  daily_step_target: number
  daily_calorie_target?: number
  daily_workout_target?: number
  avatar_url?: string | null
  is_complete?: boolean
}): Profile {
  return {
    heightCm: p.height_cm,
    weightKg: p.weight_kg,
    age: p.age,
    fitnessLevel: p.fitness_level,
    dailyStepTarget: p.daily_step_target,
    dailyCalorieTarget: p.daily_calorie_target ?? 500,
    dailyWorkoutTarget: p.daily_workout_target ?? 1,
    avatarUrl: p.avatar_url ?? null,
    isComplete: p.is_complete ?? false,
  }
}

function mapActivity(a: {
  id: string
  activity_type: string
  category: string
  title: string
  steps: number
  duration_minutes: number
  calories_burned: number
  notes: string
  logged_at: string
}): Activity {
  return {
    id: a.id,
    activityType: a.activity_type as Activity['activityType'],
    category: a.category,
    title: a.title,
    steps: a.steps,
    durationMinutes: a.duration_minutes,
    caloriesBurned: a.calories_burned,
    notes: a.notes,
    loggedAt: a.logged_at,
  }
}

function mapGoal(g: {
  id: string
  metric: string
  period: string
  target_value: number
  start_date: string
  end_date: string | null
  is_active: boolean
  current_value: number
  progress_percent: number
}): Goal {
  return {
    id: g.id,
    metric: g.metric as Goal['metric'],
    period: g.period as Goal['period'],
    targetValue: g.target_value,
    startDate: g.start_date,
    endDate: g.end_date,
    isActive: g.is_active,
    currentValue: g.current_value,
    progressPercent: g.progress_percent,
  }
}

function mapNotification(n: {
  id: string
  title: string
  body: string
  kind: string
  is_read: boolean
  created_at: string
}): Notification {
  return {
    id: n.id,
    title: n.title,
    body: n.body,
    kind: n.kind,
    isRead: n.is_read,
    createdAt: n.created_at,
  }
}

function mapDashboard(d: {
  today_steps: number
  today_calories: number
  today_workouts: number
  week_steps: number
  week_calories: number
  week_workouts: number
  active_goals: Parameters<typeof mapGoal>[0][]
  streak_days: number
}): Dashboard {
  return {
    todaySteps: d.today_steps,
    todayCalories: d.today_calories,
    todayWorkouts: d.today_workouts,
    weekSteps: d.week_steps,
    weekCalories: d.week_calories,
    weekWorkouts: d.week_workouts,
    activeGoals: d.active_goals.map(mapGoal),
    streakDays: d.streak_days,
  }
}

/* --- auth --- */

export async function fetchMeApi(): Promise<User> {
  const u = await apiJson<{ id: string; name: string; email: string; role: User['role'] }>('/api/auth/me')
  return { id: u.id, name: u.name, email: u.email, role: u.role }
}

export async function loginApi(email: string, password: string): Promise<string> {
  const res = await apiJson<{ access_token: string }>('/api/auth/login', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  })
  return res.access_token
}

export async function registerApi(name: string, email: string, password: string): Promise<string> {
  const res = await apiJson<{ access_token: string }>('/api/auth/register', {
    method: 'POST',
    body: JSON.stringify({ name, email, password }),
  })
  return res.access_token
}

export async function fetchProfileApi(): Promise<Profile> {
  return mapProfile(await apiJson('/api/auth/profile'))
}

export async function updateProfileApi(payload: Partial<{
  height_cm: number
  weight_kg: number
  age: number
  fitness_level: string
  daily_step_target: number
  daily_calorie_target: number
  daily_workout_target: number
}>): Promise<Profile> {
  return mapProfile(await apiJson('/api/auth/profile', { method: 'PATCH', body: JSON.stringify(payload) }))
}

export async function uploadAvatarApi(file: File): Promise<Profile> {
  const url = `${API_BASE}/api/auth/profile/avatar`
  const headers = new Headers()
  const token = localStorage.getItem(STORAGE_KEYS.accessToken)
  if (token) headers.set('Authorization', `Bearer ${token}`)
  const res = await fetch(url, { method: 'POST', headers, body: (() => {
    const fd = new FormData()
    fd.append('file', file)
    return fd
  })() })
  const text = await res.text()
  const data = text ? JSON.parse(text) : null
  if (!res.ok) throw new Error(formatError(res, data))
  return mapProfile(data)
}

/* --- activities --- */

export async function fetchActivitiesApi(): Promise<Activity[]> {
  const rows = await apiJson<Parameters<typeof mapActivity>[0][]>('/api/activities')
  return rows.map(mapActivity)
}

export async function createActivityApi(body: Record<string, unknown>): Promise<Activity> {
  return mapActivity(await apiJson('/api/activities', { method: 'POST', body: JSON.stringify(body) }))
}

export async function syncStepsApi(steps: number): Promise<Activity> {
  return mapActivity(
    await apiJson('/api/activities/steps/sync', { method: 'POST', body: JSON.stringify({ steps }) }),
  )
}

export async function deleteActivityApi(id: string): Promise<void> {
  await apiJson(`/api/activities/${id}`, { method: 'DELETE' })
}

/* --- goals --- */

export async function fetchGoalsApi(activeOnly = false): Promise<Goal[]> {
  const q = activeOnly ? '?active_only=true' : ''
  const rows = await apiJson<Parameters<typeof mapGoal>[0][]>(`/api/goals${q}`)
  return rows.map(mapGoal)
}

export async function createGoalApi(body: {
  metric: string
  period: string
  target_value: number
}): Promise<Goal> {
  return mapGoal(await apiJson('/api/goals', { method: 'POST', body: JSON.stringify(body) }))
}

export async function updateGoalApi(
  id: string,
  body: { target_value?: number; is_active?: boolean },
): Promise<Goal> {
  return mapGoal(await apiJson(`/api/goals/${id}`, { method: 'PATCH', body: JSON.stringify(body) }))
}

export async function deleteGoalApi(id: string): Promise<void> {
  await apiJson(`/api/goals/${id}`, { method: 'DELETE' })
}

/* --- analytics --- */

export async function fetchDashboardApi(): Promise<Dashboard> {
  return mapDashboard(await apiJson('/api/analytics/dashboard'))
}

export async function fetchTrendsApi(days = 14): Promise<TrendPoint[]> {
  const res = await apiJson<{ points: { date: string; steps: number; calories: number; workouts: number }[] }>(
    `/api/analytics/trends?days=${days}`,
  )
  return res.points.map((p) => ({
    date: p.date,
    steps: p.steps,
    calories: p.calories,
    workouts: p.workouts,
  }))
}

/* --- notifications --- */

export async function fetchNotificationsApi(): Promise<Notification[]> {
  const rows = await apiJson<Parameters<typeof mapNotification>[0][]>('/api/notifications')
  return rows.map(mapNotification)
}

export async function markNotificationReadApi(id: string): Promise<Notification> {
  return mapNotification(await apiJson(`/api/notifications/${id}/read`, { method: 'PATCH' }))
}

export async function markAllNotificationsReadApi(): Promise<void> {
  await apiJson('/api/notifications/mark-all-read', { method: 'POST' })
}

export async function createReminderApi(title: string, body: string): Promise<Notification> {
  return mapNotification(
    await apiJson('/api/notifications', {
      method: 'POST',
      body: JSON.stringify({ title, body, kind: 'reminder' }),
    }),
  )
}

/* --- admin --- */

export async function fetchAdminStatsApi(): Promise<AdminStats> {
  const s = await apiJson<{
    total_users: number
    total_activities: number
    total_goals: number
    active_members: number
    today_platform_steps: number
    today_platform_calories: number
    today_platform_workouts: number
    profiles_complete: number
  }>('/api/admin/stats')
  return {
    totalUsers: s.total_users,
    totalActivities: s.total_activities,
    totalGoals: s.total_goals,
    activeMembers: s.active_members,
    todayPlatformSteps: s.today_platform_steps,
    todayPlatformCalories: s.today_platform_calories,
    todayPlatformWorkouts: s.today_platform_workouts,
    profilesComplete: s.profiles_complete,
  }
}

export async function fetchAdminUsersApi(): Promise<AdminUser[]> {
  const rows = await apiJson<
    {
      id: string
      name: string
      email: string
      role: string
      avatar_url: string | null
      fitness_level: string | null
      profile_complete: boolean
      daily_step_target: number
      daily_calorie_target: number
      daily_workout_target: number
      today_steps: number
      today_calories: number
      today_workouts: number
      streak_days: number
      total_activities: number
      total_goals: number
      last_active: string | null
      active_goals: {
        id: string
        metric: string
        period: string
        target_value: number
        start_date: string
        end_date: string | null
        is_active: boolean
        current_value: number
        progress_percent: number
      }[]
      recent_activities: Parameters<typeof mapActivity>[0][]
    }[]
  >('/api/admin/users/overview')
  return rows.map((u) => ({
    id: u.id,
    name: u.name,
    email: u.email,
    role: u.role,
    avatarUrl: u.avatar_url,
    fitnessLevel: u.fitness_level,
    profileComplete: u.profile_complete,
    dailyStepTarget: u.daily_step_target,
    dailyCalorieTarget: u.daily_calorie_target,
    dailyWorkoutTarget: u.daily_workout_target,
    todaySteps: u.today_steps,
    todayCalories: u.today_calories,
    todayWorkouts: u.today_workouts,
    streakDays: u.streak_days,
    totalActivities: u.total_activities,
    totalGoals: u.total_goals,
    lastActive: u.last_active,
    activeGoals: u.active_goals.map(mapGoal),
    recentActivities: u.recent_activities.map(mapActivity),
  }))
}

export async function fetchAdminActivitiesApi(): Promise<Activity[]> {
  const rows = await apiJson<Parameters<typeof mapActivity>[0][]>('/api/admin/activities')
  return rows.map(mapActivity)
}
