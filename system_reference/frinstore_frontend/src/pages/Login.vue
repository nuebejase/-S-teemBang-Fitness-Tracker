<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import { ArrowLeft } from 'lucide-vue-next'
import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import { useAppStore } from '@/stores/appStore'
import { toast } from 'vue-sonner'

const router = useRouter()
const route = useRoute()
const appStore = useAppStore()

const email = ref('')
const password = ref('')

const handleSubmit = async () => {
  try {
    await appStore.login(email.value, password.value)
    toast.success('Login successful!')
    const raw = route.query.redirect
    const redirect =
      typeof raw === 'string' && raw.startsWith('/') && !raw.startsWith('//')
        ? raw
        : null
    if (redirect) {
      router.push(redirect)
    } else if (appStore.user?.role === 'admin') {
      router.push('/admin')
    } else {
      router.push('/')
    }
  } catch {
    toast.error('Invalid email or password')
  }
}
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-pink-100 via-pink-200 to-pink-300 flex items-center justify-center py-12 px-4">
    <Card class="w-full max-w-md p-8 border-pink-200">
      <div class="mb-6">
        <RouterLink
          to="/"
          class="inline-flex items-center gap-2 text-sm font-medium text-pink-700 hover:text-pink-900 hover:underline"
        >
          <ArrowLeft class="w-4 h-4 shrink-0" aria-hidden="true" />
          Back to homepage
        </RouterLink>
      </div>
      <div class="text-center mb-8">
        <div
          class="w-20 h-20 bg-gradient-to-br from-pink-500 to-pink-600 rounded-full flex items-center justify-center mx-auto mb-4"
        >
          <span class="text-4xl" aria-hidden="true">🍦</span>
        </div>
        <h1 class="text-3xl font-bold text-gray-900 mb-2">Welcome Back!</h1>
        <p class="text-gray-600">Sign in to your FrinStore account</p>
      </div>

      <form class="space-y-4" @submit.prevent="handleSubmit">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1" for="login-email">Email</label>
          <input
            id="login-email"
            v-model="email"
            type="email"
            required
            autocomplete="email"
            placeholder="your@email.com"
            class="w-full px-3 py-2 rounded-md border border-pink-200 bg-background text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1" for="login-password">Password</label>
          <input
            id="login-password"
            v-model="password"
            type="password"
            required
            autocomplete="current-password"
            placeholder="••••••••"
            class="w-full px-3 py-2 rounded-md border border-pink-200 bg-background text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          />
        </div>
        <Button
          type="submit"
          class="w-full bg-gradient-to-r from-pink-500 to-pink-600 hover:from-pink-600 hover:to-pink-700 h-11"
        >
          Sign In
        </Button>
      </form>

      <div class="mt-6 text-center">
        <p class="text-gray-600">
          Don't have an account?
          <RouterLink to="/register" class="text-pink-600 font-medium hover:underline">Sign up</RouterLink>
        </p>
      </div>

      <div class="mt-6 p-4 bg-pink-50 rounded-lg">
        <p class="text-sm font-medium text-gray-900 mb-2">Demo Credentials:</p>
        <p class="text-xs text-gray-600">
          Admin: admin@frinstore.com / admin123<br />
          Customer: register on Sign Up, then sign in with your email / password
        </p>
      </div>
    </Card>
  </div>
</template>
