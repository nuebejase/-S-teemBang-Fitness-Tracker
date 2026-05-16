<script setup lang="ts">
import { computed, ref } from 'vue'
import { RouterLink, RouterView, useRoute, useRouter } from 'vue-router'
import Button from '@/components/ui/Button.vue'
import { useAppStore } from '@/stores/appStore'
import {
  Activity,
  BarChart3,
  Bell,
  Home,
  LogOut,
  Menu,
  Target,
  User,
  X,
  Dumbbell,
} from 'lucide-vue-next'

const appStore = useAppStore()
const route = useRoute()
const router = useRouter()
const mobileOpen = ref(false)

const user = computed(() => appStore.user)
const unread = computed(() => appStore.unreadCount)

const memberLinks = [
  { path: '/', label: 'Dashboard', icon: Home },
  { path: '/workouts', label: 'Log Workout', icon: Dumbbell },
  { path: '/activities', label: 'Activity', icon: Activity },
  { path: '/goals', label: 'Goals', icon: Target },
  { path: '/analytics', label: 'Analytics', icon: BarChart3 },
]

const adminLinks = [{ path: '/admin', label: 'Admin', icon: BarChart3 }]

const links = computed(() => (user.value?.role === 'admin' ? adminLinks : memberLinks))

function isActive(path: string) {
  if (path === '/') return route.path === '/'
  return route.path.startsWith(path)
}

function logout() {
  appStore.logout()
  router.push('/')
  mobileOpen.value = false
}
</script>

<template>
  <div class="min-h-screen flex flex-col bg-background">
    <header class="sticky top-0 z-50 border-b bg-white/90 backdrop-blur-md shadow-sm">
      <div class="container mx-auto px-4 h-16 flex items-center justify-between">
        <RouterLink to="/" class="flex items-center gap-2" @click="mobileOpen = false">
          <div
            class="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center text-white font-bold text-sm"
          >
            SB
          </div>
          <span class="font-bold text-lg">
            <span class="text-emerald-600">(S)</span>TeemBang
          </span>
        </RouterLink>

        <nav class="hidden md:flex items-center gap-1">
          <RouterLink
            v-for="link in links"
            :key="link.path"
            :to="link.path"
            class="flex items-center gap-1.5 px-3 py-2 rounded-lg text-sm font-medium transition-colors"
            :class="isActive(link.path) ? 'bg-emerald-50 text-emerald-700' : 'text-gray-600 hover:bg-gray-50'"
          >
            <component :is="link.icon" class="w-4 h-4" />
            {{ link.label }}
          </RouterLink>
        </nav>

        <div class="flex items-center gap-2">
          <RouterLink
            v-if="user && user.role === 'member'"
            to="/notifications"
            class="relative hidden md:block"
          >
            <Button variant="ghost" size="icon" aria-label="Notifications">
              <Bell class="w-5 h-5" />
              <span
                v-if="unread > 0"
                class="absolute -top-0.5 -right-0.5 min-w-[1.1rem] h-[1.1rem] px-1 rounded-full bg-accent text-white text-[10px] flex items-center justify-center"
              >
                {{ unread }}
              </span>
            </Button>
          </RouterLink>

          <template v-if="user">
            <RouterLink :to="user.role === 'admin' ? '/admin' : '/profile'" class="hidden md:block">
              <Button variant="ghost" size="icon" aria-label="Profile"><User class="w-5 h-5" /></Button>
            </RouterLink>
            <Button variant="ghost" size="icon" class="hidden md:flex" aria-label="Logout" @click="logout">
              <LogOut class="w-5 h-5" />
            </Button>
          </template>
          <template v-else>
            <RouterLink to="/login" class="hidden md:block">
              <Button variant="outline" size="sm">Login</Button>
            </RouterLink>
            <RouterLink to="/register" class="hidden md:block">
              <Button size="sm">Sign up</Button>
            </RouterLink>
          </template>

          <Button variant="ghost" size="icon" class="md:hidden" @click="mobileOpen = !mobileOpen">
            <X v-if="mobileOpen" class="w-5 h-5" />
            <Menu v-else class="w-5 h-5" />
          </Button>
        </div>
      </div>

      <div v-if="mobileOpen" class="md:hidden border-t px-4 py-3 space-y-1 bg-white">
        <RouterLink
          v-for="link in links"
          :key="link.path"
          :to="link.path"
          class="flex items-center gap-2 px-3 py-2 rounded-lg"
          :class="isActive(link.path) ? 'bg-emerald-50 text-emerald-700' : 'text-gray-700'"
          @click="mobileOpen = false"
        >
          <component :is="link.icon" class="w-5 h-5" />
          {{ link.label }}
        </RouterLink>
        <RouterLink
          v-if="user?.role === 'member'"
          to="/notifications"
          class="flex items-center gap-2 px-3 py-2 text-gray-700"
          @click="mobileOpen = false"
        >
          <Bell class="w-5 h-5" /> Notifications
          <span v-if="unread" class="text-accent text-sm">({{ unread }})</span>
        </RouterLink>
        <RouterLink
          v-if="user"
          :to="user.role === 'admin' ? '/admin' : '/profile'"
          class="flex items-center gap-2 px-3 py-2 text-gray-700"
          @click="mobileOpen = false"
        >
          <User class="w-5 h-5" /> Profile
        </RouterLink>
        <button v-if="user" type="button" class="flex items-center gap-2 px-3 py-2 w-full text-left" @click="logout">
          <LogOut class="w-5 h-5" /> Logout
        </button>
        <div v-else class="flex gap-2 pt-2">
          <RouterLink to="/login" class="flex-1" @click="mobileOpen = false">
            <Button variant="outline" class="w-full">Login</Button>
          </RouterLink>
          <RouterLink to="/register" class="flex-1" @click="mobileOpen = false">
            <Button class="w-full">Sign up</Button>
          </RouterLink>
        </div>
      </div>
    </header>

    <main class="flex-1">
      <RouterView />
    </main>

    <footer class="border-t mt-auto py-6 bg-white">
      <div class="container mx-auto px-4 text-center text-sm text-muted-foreground">
        © 2026 (S)TeemBang · Group 4 · Fitness Tracking Application
      </div>
    </footer>
  </div>
</template>
