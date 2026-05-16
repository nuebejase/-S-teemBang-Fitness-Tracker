<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { ArrowLeft } from 'lucide-vue-next'
import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import { useAppStore } from '@/stores/appStore'
import { toast } from 'vue-sonner'

const router = useRouter()
const appStore = useAppStore()

const name = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')

const handleSubmit = async () => {
  if (password.value !== confirmPassword.value) {
    toast.error('Passwords do not match')
    return
  }
  if (password.value.length < 6) {
    toast.error('Password must be at least 6 characters')
    return
  }

  try {
    await appStore.register(name.value.trim(), email.value.trim().toLowerCase(), password.value)
    toast.success('Registration successful!')
    router.push('/')
  } catch (e) {
    const msg = e instanceof Error ? e.message : 'Registration failed. Please try again.'
    toast.error(msg)
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
        <h1 class="text-3xl font-bold text-gray-900 mb-2">Join FrinStore</h1>
        <p class="text-gray-600">Create your account to start ordering</p>
      </div>

      <form class="space-y-4" @submit.prevent="handleSubmit">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1" for="reg-name">Full Name</label>
          <input
            id="reg-name"
            v-model="name"
            type="text"
            required
            autocomplete="name"
            placeholder="Juan Dela Cruz"
            class="w-full px-3 py-2 rounded-md border border-pink-200 bg-background text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1" for="reg-email">Email</label>
          <input
            id="reg-email"
            v-model="email"
            type="email"
            required
            autocomplete="email"
            placeholder="your@email.com"
            class="w-full px-3 py-2 rounded-md border border-pink-200 bg-background text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1" for="reg-password">Password</label>
          <input
            id="reg-password"
            v-model="password"
            type="password"
            required
            autocomplete="new-password"
            placeholder="••••••••"
            class="w-full px-3 py-2 rounded-md border border-pink-200 bg-background text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1" for="reg-confirm">Confirm Password</label>
          <input
            id="reg-confirm"
            v-model="confirmPassword"
            type="password"
            required
            autocomplete="new-password"
            placeholder="••••••••"
            class="w-full px-3 py-2 rounded-md border border-pink-200 bg-background text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          />
        </div>
        <Button
          type="submit"
          class="w-full bg-gradient-to-r from-pink-500 to-pink-600 hover:from-pink-600 hover:to-pink-700 h-11"
        >
          Create Account
        </Button>
      </form>

      <div class="mt-6 text-center">
        <p class="text-gray-600">
          Already have an account?
          <RouterLink to="/login" class="text-pink-600 font-medium hover:underline">Sign in</RouterLink>
        </p>
      </div>
    </Card>
  </div>
</template>
