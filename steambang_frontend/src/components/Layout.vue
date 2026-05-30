<script setup lang="ts">
import { computed, ref } from 'vue'
import { RouterLink, RouterView, useRoute, useRouter } from 'vue-router'
import Button from '@/components/ui/Button.vue'
import Avatar from '@/components/Avatar.vue'
import { useAppStore } from '@/stores/appStore'
import {
  BarChart3,
  Bell,
  Home,
  LogOut,
  Shield,
  Target,
  User,
  Dumbbell,
} from 'lucide-vue-next'

const appStore = useAppStore()
const route = useRoute()
const router = useRouter()
const mobileOpen = ref(false)

const user = computed(() => appStore.user)
const unread = computed(() => appStore.unreadCount)
const isAdmin = computed(() => user.value?.role === 'admin')

const memberLinks = [
  { path: '/', label: 'Home', icon: Home },
  { path: '/workouts', label: 'Train', icon: Dumbbell },
  { path: '/goals', label: 'Goals', icon: Target },
  { path: '/analytics', label: 'Stats', icon: BarChart3 },
  { path: '/profile', label: 'Profile', icon: User },
]

const adminLinks = [{ path: '/admin', label: 'Overview', icon: Shield }]

const links = computed(() => (isAdmin.value ? adminLinks : memberLinks))

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
  <div :class="['min-h-screen flex flex-col', isAdmin ? 'admin-shell' : 'app-shell']">
    <header class="sticky top-0 z-50 border-b border-white/[0.06] bg-background/70 backdrop-blur-2xl">
      <div class="container mx-auto px-4 h-16 flex items-center justify-between max-w-6xl">
        <RouterLink to="/" class="flex items-center gap-3" @click="mobileOpen = false">
          <div
            class="w-10 h-10 rounded-2xl flex items-center justify-center text-white font-bold text-sm shadow-lg"
            :class="isAdmin ? 'bg-gradient-to-br from-violet-500 to-fuchsia-600' : 'bg-gradient-to-br from-emerald-500 to-teal-600'"
          >
            SB
          </div>
          <div>
            <span class="font-bold text-lg tracking-tight">
              <span :class="isAdmin ? 'gradient-text-admin' : 'gradient-text'">(S)</span>TeemBang
            </span>
            <p v-if="isAdmin" class="text-[10px] uppercase tracking-widest text-muted-foreground -mt-0.5">Admin</p>
          </div>
        </RouterLink>

        <nav v-if="user" class="hidden md:flex items-center gap-1">
          <RouterLink
            v-for="link in links"
            :key="link.path"
            :to="link.path"
            class="flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-medium transition-all"
            :class="
              isActive(link.path)
                ? isAdmin
                  ? 'bg-violet-500/15 text-violet-300 border border-violet-500/20'
                  : 'bg-emerald-500/15 text-emerald-300 border border-emerald-500/20'
                : 'text-muted-foreground hover:text-foreground hover:bg-white/[0.04]'
            "
          >
            <component :is="link.icon" class="w-4 h-4" />
            {{ link.label }}
          </RouterLink>
        </nav>

        <div class="flex items-center gap-2">
          <RouterLink v-if="user && !isAdmin" to="/notifications" class="relative hidden md:block">
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
            <RouterLink :to="isAdmin ? '/admin' : '/profile'" class="hidden md:flex items-center gap-2">
              <Avatar :name="user.name" :src="appStore.profile?.avatarUrl" size="sm" />
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
        </div>
      </div>
    </header>

    <!-- Mobile bottom tab bar -->
    <nav
      v-if="user"
      class="md:hidden fixed bottom-0 inset-x-0 z-50 border-t border-white/[0.06] bg-background/90 backdrop-blur-2xl pb-safe"
    >
      <div class="flex justify-around items-center h-16 px-2">
        <RouterLink
          v-for="link in links"
          :key="link.path"
          :to="link.path"
          class="flex flex-col items-center gap-0.5 px-3 py-1 rounded-xl min-w-[3.5rem]"
          :class="isActive(link.path) ? (isAdmin ? 'text-violet-400' : 'text-emerald-400') : 'text-muted-foreground'"
        >
          <component :is="link.icon" class="w-5 h-5" />
          <span class="text-[10px] font-medium">{{ link.label }}</span>
        </RouterLink>
        <RouterLink
          v-if="!isAdmin"
          to="/notifications"
          class="flex flex-col items-center gap-0.5 px-3 py-1 text-muted-foreground relative"
        >
          <Bell class="w-5 h-5" />
          <span class="text-[10px] font-medium">Alerts</span>
          <span
            v-if="unread"
            class="absolute top-0 right-1 w-4 h-4 rounded-full bg-accent text-[9px] text-white flex items-center justify-center"
          >
            {{ unread }}
          </span>
        </RouterLink>
      </div>
    </nav>

    <main class="flex-1 pb-20 md:pb-0">
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
.pb-safe {
  padding-bottom: env(safe-area-inset-bottom, 0);
}
</style>
