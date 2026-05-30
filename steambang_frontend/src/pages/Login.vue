<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import { useAppStore } from '@/stores/appStore'
import { toast } from 'vue-sonner'

const router = useRouter()
const route = useRoute()
const store = useAppStore()
const email = ref('')
const password = ref('')
const loading = ref(false)

async function submit() {
  loading.value = true
  try {
    await store.login(email.value, password.value)
    toast.success('Welcome back!')
    const redirect = typeof route.query.redirect === 'string' ? route.query.redirect : null
    router.push(redirect && redirect.startsWith('/') ? redirect : store.user?.role === 'admin' ? '/admin' : '/')
  } catch {
    toast.error('Invalid email or password')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen app-shell flex items-center justify-center px-4 py-12">
    <Card class="w-full max-w-md p-8 md:p-10">
      <div class="text-center mb-8">
        <div class="w-16 h-16 mx-auto rounded-2xl bg-gradient-to-br from-emerald-500 to-teal-600 text-white flex items-center justify-center font-bold text-xl mb-5 shadow-lg btn-glow">
          SB
        </div>
        <h1 class="text-2xl font-bold tracking-tight">Welcome back</h1>
        <p class="text-muted-foreground text-sm mt-2">Sign in to your fitness dashboard</p>
      </div>
      <form class="space-y-5" @submit.prevent="submit">
        <div>
          <label class="premium-label" for="email">Email</label>
          <input id="email" v-model="email" type="email" required class="premium-input mt-2" placeholder="you@example.com" />
        </div>
        <div>
          <label class="premium-label" for="pw">Password</label>
          <input id="pw" v-model="password" type="password" required class="premium-input mt-2" placeholder="••••••••" />
        </div>
        <Button type="submit" class="w-full" size="lg" :disabled="loading">
          {{ loading ? 'Signing in…' : 'Sign in' }}
        </Button>
      </form>
      <p class="text-center text-sm mt-8 text-muted-foreground">
        No account?
        <RouterLink to="/register" class="text-emerald-400 font-medium hover:underline">Create one</RouterLink>
      </p>
      <div class="mt-6 p-3 rounded-xl bg-white/[0.03] border border-white/[0.06] text-xs text-muted-foreground text-center space-y-1">
        <p>Demo: demo@steambang.com / demo1234</p>
        <p>Admin: admin@steambang.com / admin123</p>
      </div>
    </Card>
  </div>
</template>
