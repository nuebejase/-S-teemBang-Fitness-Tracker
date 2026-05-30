<script setup lang="ts">
import { ref } from 'vue'
import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import { useAppStore } from '@/stores/appStore'
import { formatDateTime } from '@/lib/utils'
import { toast } from 'vue-sonner'
import { Trophy, Bell } from 'lucide-vue-next'

const store = useAppStore()
const title = ref('')
const body = ref('')

function displayBody(text: string) {
  return text.replace(/^goal:\d+:\d{4}-\d{2}-\d{2}\n?/, '')
}

async function markAll() {
  await store.markAllRead()
  toast.success('All marked read')
}

async function markOne(id: string) {
  await store.markRead(id)
}

async function addReminder() {
  if (!title.value.trim()) return
  try {
    await store.addReminder(title.value, body.value)
    title.value = ''
    body.value = ''
    toast.success('Reminder created')
  } catch (e) {
    toast.error(e instanceof Error ? e.message : 'Failed')
  }
}
</script>

<template>
  <div class="container mx-auto px-4 py-8 max-w-2xl space-y-6">
    <div class="flex justify-between items-center">
      <h1 class="text-2xl font-bold">Notifications</h1>
      <Button variant="outline" size="sm" @click="markAll">Mark all read</Button>
    </div>
    <Card class="p-4 space-y-3">
      <h2 class="font-semibold text-sm">Create reminder</h2>
      <input v-model="title" class="w-full px-3 py-2 rounded-lg border" placeholder="Title" />
      <textarea v-model="body" rows="2" class="w-full px-3 py-2 rounded-lg border" placeholder="Message" />
      <Button size="sm" @click="addReminder">Add reminder</Button>
    </Card>
    <div class="space-y-2">
      <Card
        v-for="n in store.notifications"
        :key="n.id"
        class="p-4 cursor-pointer"
        :class="!n.isRead ? (n.kind === 'achievement' ? 'border-amber-400/50 bg-amber-500/10' : 'border-emerald-400/40 bg-emerald-500/10') : ''"
        @click="markOne(n.id)"
      >
        <div class="flex items-start gap-2">
          <Trophy v-if="n.kind === 'achievement'" class="w-5 h-5 text-amber-400 shrink-0 mt-0.5" />
          <Bell v-else class="w-5 h-5 text-emerald-400 shrink-0 mt-0.5" />
          <div class="flex-1 min-w-0">
            <p class="font-medium">{{ n.title }}</p>
            <p class="text-sm text-muted-foreground mt-1">{{ displayBody(n.body) }}</p>
            <p class="text-xs text-muted-foreground mt-2">{{ formatDateTime(n.createdAt) }}</p>
          </div>
        </div>
      </Card>
    </div>
  </div>
</template>
