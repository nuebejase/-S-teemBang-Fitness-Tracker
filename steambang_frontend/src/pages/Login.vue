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

async function submit() {
  try {
    await store.login(email.value, password.value)
    toast.success('Welcome back!')
    const redirect = typeof route.query.redirect === 'string' ? route.query.redirect : null
    router.push(redirect && redirect.startsWith('/') ? redirect : store.user?.role === 'admin' ? '/admin' : '/')
  } catch {
    toast.error('Invalid email or password')
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-emerald-100 to-teal-200 px-4 py-12">
    <Card class="w-full max-w-md p-8">
      <div class="text-center mb-8">
        <div class="w-16 h-16 mx-auto rounded-2xl bg-gradient-to-br from-emerald-500 to-teal-600 text-white flex items-center justify-center font-bold text-xl mb-4">SB</div>
        <h1 class="text-2xl font-bold">Sign in</h1>
        <p class="text-muted-foreground text-sm mt-1">(S)TeemBang fitness tracker</p>
      </div>
      <form class="space-y-4" @submit.prevent="submit">
        <div>
          <label class="text-sm font-medium" for="email">Email</label>
          <input id="email" v-model="email" type="email" required class="mt-1 w-full px-3 py-2 rounded-lg border" />
        </div>
        <div>
          <label class="text-sm font-medium" for="pw">Password</label>
          <input id="pw" v-model="password" type="password" required class="mt-1 w-full px-3 py-2 rounded-lg border" />
        </div>
        <Button type="submit" class="w-full">Sign in</Button>
      </form>
      <p class="text-center text-sm mt-6 text-muted-foreground">
        No account?
        <RouterLink to="/register" class="text-emerald-600 font-medium hover:underline">Register</RouterLink>
      </p>
      <p class="text-xs text-center mt-4 text-muted-foreground">Demo: demo@steambang.com / demo1234</p>
    </Card>
  </div>
</template>
