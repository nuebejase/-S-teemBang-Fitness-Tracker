<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import { useAppStore } from '@/stores/appStore'
import type { OrderStatus } from '@/types/domain'
import { Package, Clock, Truck, CheckCircle, XCircle } from 'lucide-vue-next'

const appStore = useAppStore()

onMounted(() => {
  void appStore.refreshOrders()
})

const userOrders = computed(() => {
  if (!appStore.user) return []
  return appStore.orders.filter((order) => order.customerEmail === appStore.user?.email)
})

const statusConfig: Record<
  Exclude<OrderStatus, 'cancelled'>,
  { label: string; color: string; icon: typeof Clock }
> = {
  pending: { label: 'Pending', color: 'bg-yellow-100 text-yellow-800', icon: Clock },
  processing: { label: 'Processing', color: 'bg-blue-100 text-blue-800', icon: Package },
  shipped: { label: 'Shipped', color: 'bg-purple-100 text-purple-800', icon: Truck },
  delivered: { label: 'Delivered', color: 'bg-green-100 text-green-800', icon: CheckCircle },
}

const timelineKeys: Exclude<OrderStatus, 'cancelled'>[] = [
  'pending',
  'processing',
  'shipped',
  'delivered',
]

const statusDisplay = (status: OrderStatus) => {
  if (status === 'cancelled') {
    return { label: 'Cancelled', color: 'bg-red-100 text-red-800', icon: XCircle }
  }
  return statusConfig[status]
}

const timelineIndex = (status: OrderStatus) => {
  if (status === 'cancelled') return -1
  return timelineKeys.indexOf(status)
}
</script>

<template>
  <div v-if="userOrders.length === 0" class="min-h-screen bg-gradient-to-b from-pink-50 to-white flex items-center justify-center">
    <div class="text-center py-20 px-4">
      <div class="text-8xl mb-6" aria-hidden="true">📦</div>
      <h2 class="text-3xl font-bold text-gray-900 mb-4">No Orders Yet</h2>
      <p class="text-gray-600 mb-8">You haven't placed any orders yet.</p>
      <RouterLink to="/products">
        <Button class="bg-gradient-to-r from-pink-500 to-pink-600 hover:from-pink-600 hover:to-pink-700">
          Browse products
        </Button>
      </RouterLink>
    </div>
  </div>

  <div v-else class="min-h-screen bg-gradient-to-b from-pink-50 to-white py-8">
    <div class="container mx-auto px-4">
      <h1 class="text-4xl font-bold text-gray-900 mb-8">My Orders</h1>

      <div class="space-y-6">
        <Card v-for="order in userOrders" :key="order.id" class="p-6 border-pink-200">
          <div class="flex flex-col md:flex-row md:items-center justify-between mb-4 gap-4">
            <div>
              <h3 class="text-xl font-bold text-gray-900">Order #{{ order.id }}</h3>
              <p class="text-sm text-gray-600">
                {{
                  new Date(order.date).toLocaleDateString('en-US', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit',
                  })
                }}
              </p>
            </div>
            <span
              class="inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-medium w-fit"
              :class="statusDisplay(order.status).color"
            >
              <component :is="statusDisplay(order.status).icon" class="w-4 h-4" />
              {{ statusDisplay(order.status).label }}
            </span>
          </div>

          <div class="space-y-3 mb-4">
            <div
              v-for="item in order.items"
              :key="item.id"
              class="flex items-center gap-4 bg-pink-50 p-3 rounded-lg"
            >
              <div class="w-16 h-16 rounded-lg overflow-hidden shrink-0">
                <img :src="item.image" :alt="item.name" class="w-full h-full object-cover" />
              </div>
              <div class="flex-1 min-w-0">
                <h4 class="font-bold">{{ item.name }}</h4>
                <p class="text-sm text-gray-600">Quantity: {{ item.quantity }}</p>
              </div>
              <div class="text-right shrink-0">
                <p class="font-bold text-pink-600">₱{{ (item.price * item.quantity).toFixed(2) }}</p>
              </div>
            </div>
          </div>

          <div class="border-t-2 border-pink-200 pt-4">
            <div class="grid md:grid-cols-2 gap-4 mb-3">
              <div>
                <p class="text-sm text-gray-600">Delivery Address</p>
                <p class="font-medium">{{ order.address }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-600">Phone</p>
                <p class="font-medium">{{ order.customerPhone }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-600">Payment Method</p>
                <p class="font-medium capitalize">{{ order.paymentMethod }}</p>
              </div>
            </div>
            <div class="flex justify-between items-center">
              <span class="text-lg font-bold">Total Amount</span>
              <span class="text-2xl font-bold text-pink-600">₱{{ order.total.toFixed(2) }}</span>
            </div>
          </div>

          <div v-if="order.status !== 'cancelled'" class="mt-6 bg-gradient-to-r from-pink-50 to-white p-4 rounded-lg">
            <h4 class="font-bold mb-4 text-gray-900">Order Timeline</h4>
            <div class="flex items-start justify-between gap-2">
              <div
                v-for="(key, index) in timelineKeys"
                :key="key"
                class="flex flex-col items-center flex-1"
              >
                <div
                  class="w-10 h-10 rounded-full flex items-center justify-center ring-offset-2"
                  :class="[
                    timelineIndex(order.status) >= index
                      ? 'bg-pink-500 text-white'
                      : 'bg-gray-200 text-gray-400',
                    order.status === key ? 'ring-4 ring-pink-200' : '',
                  ]"
                >
                  <component :is="statusConfig[key].icon" class="w-5 h-5" />
                </div>
                <p
                  class="text-xs mt-2 text-center leading-tight"
                  :class="
                    timelineIndex(order.status) >= index
                      ? 'text-pink-600 font-medium'
                      : 'text-gray-500'
                  "
                >
                  {{ statusConfig[key].label }}
                </p>
              </div>
            </div>
          </div>
          <div v-else class="mt-4 text-sm text-red-600 font-medium">
            This order was cancelled.
          </div>
        </Card>
      </div>
    </div>
  </div>
</template>
