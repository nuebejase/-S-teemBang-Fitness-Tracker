<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import { useAppStore } from '@/stores/appStore'
import { User, Mail, ShoppingBag, Package } from 'lucide-vue-next'

const appStore = useAppStore()

onMounted(() => {
  void appStore.refreshOrders()
})

const user = computed(() => appStore.user)
const userOrders = computed(() => {
  if (!user.value) return []
  return appStore.orders.filter((order) => order.customerEmail === user.value!.email)
})
const totalSpent = computed(() =>
  userOrders.value.reduce((sum, order) => sum + order.total, 0),
)

const statusBadgeClass = (status: string) => {
  if (status === 'delivered') return 'bg-green-100 text-green-800'
  if (status === 'shipped') return 'bg-purple-100 text-purple-800'
  if (status === 'processing') return 'bg-blue-100 text-blue-800'
  return 'bg-yellow-100 text-yellow-800'
}
</script>

<template>
  <div v-if="user" class="min-h-screen bg-gradient-to-b from-pink-50 to-white py-8">
    <div class="container mx-auto px-4">
      <h1 class="text-4xl font-bold text-gray-900 mb-8">My Profile</h1>

      <div class="grid lg:grid-cols-3 gap-6">
        <div class="lg:col-span-1">
          <Card class="p-6 border-pink-200">
            <div class="text-center mb-6">
              <div
                class="w-24 h-24 bg-gradient-to-br from-pink-500 to-pink-600 rounded-full flex items-center justify-center mx-auto mb-4"
              >
                <User class="w-12 h-12 text-white" />
              </div>
              <h2 class="text-2xl font-bold text-gray-900">{{ user.name }}</h2>
              <span
                class="inline-block mt-2 text-xs font-medium px-2 py-1 rounded-md bg-pink-100 text-pink-600 capitalize"
              >
                {{ user.role }}
              </span>
            </div>
            <div class="flex items-center space-x-3 text-gray-700">
              <Mail class="w-5 h-5 text-pink-500 shrink-0" />
              <span>{{ user.email }}</span>
            </div>
          </Card>

          <Card class="p-6 border-pink-200 mt-6">
            <h3 class="font-bold text-lg mb-4">Account Statistics</h3>
            <div class="space-y-4">
              <div class="flex items-center justify-between">
                <div class="flex items-center space-x-2">
                  <ShoppingBag class="w-5 h-5 text-pink-500" />
                  <span class="text-gray-700">Total Orders</span>
                </div>
                <span class="font-bold text-xl">{{ userOrders.length }}</span>
              </div>
              <div class="flex items-center justify-between">
                <div class="flex items-center space-x-2">
                  <Package class="w-5 h-5 text-pink-500" />
                  <span class="text-gray-700">Total Spent</span>
                </div>
                <span class="font-bold text-xl text-pink-600">₱{{ totalSpent.toFixed(2) }}</span>
              </div>
            </div>
          </Card>
        </div>

        <div class="lg:col-span-2">
          <Card class="p-6 border-pink-200">
            <div class="flex items-center justify-between mb-6">
              <h3 class="text-2xl font-bold">Recent Orders</h3>
              <RouterLink to="/orders">
                <Button variant="outline" class="border-pink-300 text-pink-600 hover:bg-pink-50">
                  View All
                </Button>
              </RouterLink>
            </div>
            <div v-if="userOrders.length > 0" class="space-y-4">
              <div
                v-for="order in userOrders.slice(0, 3)"
                :key="order.id"
                class="border-2 border-pink-200 rounded-lg p-4 hover:bg-pink-50 transition-colors"
              >
                <div class="flex justify-between items-start mb-2 gap-2">
                  <div>
                    <h4 class="font-bold">Order #{{ order.id }}</h4>
                    <p class="text-sm text-gray-600">
                      {{ new Date(order.date).toLocaleDateString() }}
                    </p>
                  </div>
                  <span
                    class="text-xs font-medium px-2 py-1 rounded-full capitalize shrink-0"
                    :class="statusBadgeClass(order.status)"
                  >
                    {{ order.status }}
                  </span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="text-sm text-gray-600">{{ order.items.length }} items</span>
                  <span class="font-bold text-pink-600">₱{{ order.total.toFixed(2) }}</span>
                </div>
              </div>
            </div>
            <div v-else class="text-center py-12">
              <div class="text-6xl mb-4" aria-hidden="true">📦</div>
              <p class="text-gray-600">No orders yet</p>
              <RouterLink to="/products" class="mt-4 inline-block">
                <Button class="bg-gradient-to-r from-pink-500 to-pink-600 hover:from-pink-600 hover:to-pink-700">
                  Start Shopping
                </Button>
              </RouterLink>
            </div>
          </Card>
        </div>
      </div>
    </div>
  </div>
</template>
