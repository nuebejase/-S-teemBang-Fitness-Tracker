export type UserRole = 'member' | 'admin'

export interface User {
  id: string
  name: string
  email: string
  role: UserRole
}

export interface Profile {
  heightCm: number | null
  weightKg: number | null
  age: number | null
  fitnessLevel: string
  dailyStepTarget: number
}

export interface Activity {
  id: string
  activityType: 'steps' | 'workout'
  category: string
  title: string
  steps: number
  durationMinutes: number
  caloriesBurned: number
  notes: string
  loggedAt: string
}

export interface Goal {
  id: string
  metric: 'steps' | 'calories' | 'workouts'
  period: 'daily' | 'weekly' | 'monthly'
  targetValue: number
  startDate: string
  endDate: string | null
  isActive: boolean
  currentValue: number
  progressPercent: number
}

export interface Notification {
  id: string
  title: string
  body: string
  kind: string
  isRead: boolean
  createdAt: string
}

export interface Dashboard {
  todaySteps: number
  todayCalories: number
  todayWorkouts: number
  weekSteps: number
  weekCalories: number
  weekWorkouts: number
  activeGoals: Goal[]
  streakDays: number
}

export interface TrendPoint {
  date: string
  steps: number
  calories: number
  workouts: number
}

export interface AdminStats {
  totalUsers: number
  totalActivities: number
  totalGoals: number
  activeMembers: number
}
