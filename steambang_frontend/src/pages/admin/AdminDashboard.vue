<script setup lang="ts">
import { onMounted } from 'vue'
import Card from '@/components/ui/Card.vue'
import StatCard from '@/components/StatCard.vue'
import { useAppStore } from '@/stores/appStore'
import { formatDateTime } from '@/lib/utils'
import { Users, Activity, Target, UserCheck } from 'lucide-vue-next'

const store = useAppStore()

onMounted(() => store.refreshAdmin())
</script>

<template>
  <div class="container mx-auto px-4 py-8 space-y-8">
    <h1 class="text-2xl font-bold">Admin dashboard</h1>
    <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <StatCard label="Total users" :value="String(store.adminStats?.totalUsers ?? 0)" :icon="Users" />
      <StatCard label="Activities logged" :value="String(store.adminStats?.totalActivities ?? 0)" :icon="Activity" />
      <StatCard label="Goals set" :value="String(store.adminStats?.totalGoals ?? 0)" :icon="Target" accent="bg-orange-100 text-orange-600" />
      <StatCard label="Active (7d)" :value="String(store.adminStats?.activeMembers ?? 0)" :icon="UserCheck" accent="bg-violet-100 text-violet-600" />
    </div>
    <Card class="p-6">
      <h2 class="font-semibold mb-4">Recent platform activity</h2>
      <div class="space-y-2 max-h-96 overflow-y-auto">
        <div v-for="a in store.activities.slice(0, 20)" :key="a.id" class="text-sm border-b py-2 flex justify-between gap-4">
          <span>{{ a.title }}</span>
          <span class="text-muted-foreground shrink-0">{{ formatDateTime(a.loggedAt) }}</span>
        </div>
        <p v-if="!store.activities.length" class="text-muted-foreground text-sm">No activity yet.</p>
      </div>
    </Card>
    <p class="text-sm text-muted-foreground">Admin: admin@steambang.com / admin123</p>
  </div>
</template>
