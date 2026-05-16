import { createRouter, createWebHistory, type RouteLocationNormalized } from 'vue-router'
import { useAppStore } from '@/stores/appStore'
import Layout from '@/components/Layout.vue'
import Dashboard from '@/pages/Dashboard.vue'
import Workouts from '@/pages/Workouts.vue'
import Activities from '@/pages/Activities.vue'
import Goals from '@/pages/Goals.vue'
import Analytics from '@/pages/Analytics.vue'
import Notifications from '@/pages/Notifications.vue'
import Profile from '@/pages/Profile.vue'
import About from '@/pages/About.vue'
import Login from '@/pages/Login.vue'
import Register from '@/pages/Register.vue'
import AdminDashboard from '@/pages/admin/AdminDashboard.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: Layout,
      children: [
        { path: '', name: 'dashboard', component: Dashboard },
        { path: 'workouts', name: 'workouts', component: Workouts, meta: { requiresAuth: true, memberOnly: true } },
        { path: 'activities', name: 'activities', component: Activities, meta: { requiresAuth: true, memberOnly: true } },
        { path: 'goals', name: 'goals', component: Goals, meta: { requiresAuth: true, memberOnly: true } },
        { path: 'analytics', name: 'analytics', component: Analytics, meta: { requiresAuth: true, memberOnly: true } },
        { path: 'notifications', name: 'notifications', component: Notifications, meta: { requiresAuth: true, memberOnly: true } },
        { path: 'profile', name: 'profile', component: Profile, meta: { requiresAuth: true } },
        { path: 'about', name: 'about', component: About },
        { path: 'admin', name: 'admin', component: AdminDashboard, meta: { requiresAuth: true, requiresAdmin: true } },
      ],
    },
    { path: '/login', name: 'login', component: Login, meta: { guestOnly: true } },
    { path: '/register', name: 'register', component: Register, meta: { guestOnly: true } },
    { path: '/:pathMatch(.*)*', redirect: '/' },
  ],
  scrollBehavior(_to, _from, saved) {
    return saved ?? { top: 0 }
  },
})

router.beforeEach((to: RouteLocationNormalized) => {
  const store = useAppStore()
  const user = store.user

  if (to.meta.guestOnly && user) {
    return { path: user.role === 'admin' ? '/admin' : '/' }
  }
  if (to.meta.requiresAuth && !user) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }
  if (to.meta.requiresAdmin && user?.role !== 'admin') {
    return { name: 'dashboard' }
  }
  if (to.meta.memberOnly && user?.role === 'admin') {
    return { name: 'admin' }
  }
  return true
})

export default router
