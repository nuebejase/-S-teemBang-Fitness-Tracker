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

async function submit() {
  try {
    await store.register(name.value, email.value, password.value)
    toast.success('Account created!')
    router.push('/')
  } catch (e) {
    toast.error(e instanceof Error ? e.message : 'Registration failed')
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-emerald-100 to-teal-200 px-4 py-12">
    <Card class="w-full max-w-md p-8">
      <h1 class="text-2xl font-bold text-center mb-6">Create account</h1>
      <form class="space-y-4" @submit.prevent="submit">
        <div>
          <label class="text-sm font-medium">Name</label>
          <input v-model="name" required class="mt-1 w-full px-3 py-2 rounded-lg border" />
        </div>
        <div>
          <label class="text-sm font-medium">Email</label>
          <input v-model="email" type="email" required class="mt-1 w-full px-3 py-2 rounded-lg border" />
        </div>
        <div>
          <label class="text-sm font-medium">Password</label>
          <input v-model="password" type="password" required minlength="6" class="mt-1 w-full px-3 py-2 rounded-lg border" />
        </div>
        <Button type="submit" class="w-full">Sign up</Button>
      </form>
      <p class="text-center text-sm mt-6">
        <RouterLink to="/login" class="text-emerald-600 hover:underline">Already have an account?</RouterLink>
      </p>
    </Card>
  </div>
</template>
