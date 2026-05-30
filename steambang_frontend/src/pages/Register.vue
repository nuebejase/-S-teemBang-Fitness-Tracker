<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import { useAppStore } from '@/stores/appStore'
import { toast } from 'vue-sonner'

const router = useRouter()
const store = useAppStore()
const name = ref('')
const email = ref('')
const password = ref('')
const loading = ref(false)

async function submit() {
  loading.value = true
  try {
    await store.register(name.value, email.value, password.value)
    toast.success('Account created!')
    router.push('/profile')
  } catch (e) {
    toast.error(e instanceof Error ? e.message : 'Registration failed')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen app-shell flex items-center justify-center px-4 py-12">
    <Card class="w-full max-w-md p-8 md:p-10">
      <div class="text-center mb-8">
        <div class="w-16 h-16 mx-auto rounded-2xl bg-gradient-to-br from-emerald-500 to-teal-600 text-white flex items-center justify-center font-bold text-xl mb-5 btn-glow">SB</div>
        <h1 class="text-2xl font-bold tracking-tight">Join (S)TeemBang</h1>
        <p class="text-muted-foreground text-sm mt-2">Start your fitness journey today</p>
      </div>
      <form class="space-y-5" @submit.prevent="submit">
        <div>
          <label class="premium-label">Full name</label>
          <input v-model="name" required class="premium-input mt-2" placeholder="Your name" />
        </div>
        <div>
          <label class="premium-label">Email</label>
          <input v-model="email" type="email" required class="premium-input mt-2" placeholder="you@example.com" />
        </div>
        <div>
          <label class="premium-label">Password</label>
          <input v-model="password" type="password" required minlength="6" class="premium-input mt-2" placeholder="Min. 6 characters" />
        </div>
        <Button type="submit" class="w-full" size="lg" :disabled="loading">{{ loading ? 'Creating…' : 'Create account' }}</Button>
      </form>
      <p class="text-center text-sm mt-8 text-muted-foreground">
        <RouterLink to="/login" class="text-emerald-400 hover:underline font-medium">Already have an account?</RouterLink>
      </p>
    </Card>
  </div>
</template>
