<script setup lang="ts">
import { computed, onMounted } from 'vue'
import Card from '@/components/ui/Card.vue'
import { useAppStore } from '@/stores/appStore'
import { Package, ShoppingCart, DollarSign, AlertTriangle } from 'lucide-vue-next'

const appStore = useAppStore()

onMounted(() => {
  void appStore.refreshOrders()
})

const totalRevenue = computed(() => appStore.orders.reduce((sum, order) => sum + order.total, 0))
const totalOrders = computed(() => appStore.orders.length)
const totalProducts = computed(() => appStore.products.length)
const lowStockProducts = computed(() => appStore.products.filter((p) => p.stock < 10).length)

const statusData = computed(() => [
  { name: 'Pending', value: appStore.orders.filter((o) => o.status === 'pending').length, color: '#FCD34D' },
  { name: 'Processing', value: appStore.orders.filter((o) => o.status === 'processing').length, color: '#60A5FA' },
  { name: 'Shipped', value: appStore.orders.filter((o) => o.status === 'shipped').length, color: '#A78BFA' },
  { name: 'Delivered', value: appStore.orders.filter((o) => o.status === 'delivered').length, color: '#34D399' },
])

const categoryData = computed(() => {
  const acc = new Map<string, number>()
  for (const order of appStore.orders) {
    for (const item of order.items) {
      const line = item.price * item.quantity
      acc.set(item.category, (acc.get(item.category) ?? 0) + line)
    }
  }
  return [...acc.entries()].map(([name, sales]) => ({ name, sales }))
})

const monthlyData = computed(() => {
  const map = new Map<string, number>()
  for (const o of appStore.orders) {
    const d = new Date(o.date)
    const key = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`
    map.set(key, (map.get(key) ?? 0) + o.total)
  }
  const keys = [...map.keys()].sort()
  const lastKeys = keys.slice(-6)
  return lastKeys.map((k) => {
    const [y, m] = k.split('-').map(Number)
    const label = new Date(y, m - 1, 1).toLocaleString('en-US', { month: 'short' })
    return { key: k, month: label, revenue: map.get(k) ?? 0 }
  })
})

const maxMonthly = computed(() => Math.max(...monthlyData.value.map((d) => d.revenue), 1))
const maxCategory = computed(() => Math.max(...categoryData.value.map((d) => d.sales), 1))
const statusTotal = computed(() => statusData.value.reduce((s, x) => s + x.value, 0))
</script>

<template>
  <div class="min-h-screen bg-gradient-to-b from-pink-50 to-white py-8">
    <div class="container mx-auto px-4">
      <div class="mb-8">
        <h1 class="text-4xl font-bold text-gray-900 mb-2">Admin Dashboard</h1>
        <p class="text-gray-600">Welcome back! Here's what's happening with your store.</p>
        <p v-if="appStore.ordersLoading" class="text-sm text-pink-600 mt-2">Refreshing orders…</p>
      </div>

      <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <Card class="p-6 border-pink-200 hover:shadow-lg transition-shadow">
          <div class="flex items-center justify-between mb-2">
            <span class="text-gray-600">Total Revenue</span>
            <div class="w-12 h-12 bg-pink-100 rounded-full flex items-center justify-center">
              <DollarSign class="w-6 h-6 text-pink-600" />
            </div>
          </div>
          <div class="text-3xl font-bold text-pink-600">₱{{ totalRevenue.toFixed(2) }}</div>
          <div class="text-gray-500 text-sm mt-2">All orders in the connected database</div>
        </Card>

        <Card class="p-6 border-pink-200 hover:shadow-lg transition-shadow">
          <div class="flex items-center justify-between mb-2">
            <span class="text-gray-600">Total Orders</span>
            <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
              <ShoppingCart class="w-6 h-6 text-blue-600" />
            </div>
          </div>
          <div class="text-3xl font-bold text-blue-600">{{ totalOrders }}</div>
          <div class="text-gray-500 text-sm mt-2">Includes every status</div>
        </Card>

        <Card class="p-6 border-pink-200 hover:shadow-lg transition-shadow">
          <div class="flex items-center justify-between mb-2">
            <span class="text-gray-600">Total Products</span>
            <div class="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center">
              <Package class="w-6 h-6 text-purple-600" />
            </div>
          </div>
          <div class="text-3xl font-bold text-purple-600">{{ totalProducts }}</div>
          <div class="text-gray-500 text-sm mt-2">Active products in catalog</div>
        </Card>

        <Card class="p-6 border-pink-200 hover:shadow-lg transition-shadow">
          <div class="flex items-center justify-between mb-2">
            <span class="text-gray-600">Low Stock Alerts</span>
            <div class="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center">
              <AlertTriangle class="w-6 h-6 text-red-600" />
            </div>
          </div>
          <div class="text-3xl font-bold text-red-600">{{ lowStockProducts }}</div>
          <div class="text-gray-500 text-sm mt-2">Products below 10 units</div>
        </Card>
      </div>

      <div class="grid lg:grid-cols-2 gap-6 mb-8">
        <Card class="p-6 border-pink-200">
          <h3 class="text-xl font-bold mb-4">Monthly Revenue</h3>
          <div
            v-if="monthlyData.length === 0"
            class="h-[300px] flex items-center justify-center text-gray-500 text-sm text-center px-4"
          >
            No orders yet — chart will populate after customers check out.
          </div>
          <div v-else class="flex items-end justify-between gap-2 h-[300px] pt-4 border-b border-pink-100">
            <div
              v-for="row in monthlyData"
              :key="row.key"
              class="flex flex-col items-center flex-1 h-full justify-end"
            >
              <div
                class="w-full max-w-[48px] mx-auto rounded-t-md bg-pink-500 transition-all"
                :style="{ height: `${(row.revenue / maxMonthly) * 100}%`, minHeight: '8px' }"
                :title="`₱${row.revenue.toLocaleString()}`"
              />
              <span class="text-xs text-gray-600 mt-2">{{ row.month }}</span>
            </div>
          </div>
          <p class="text-xs text-gray-500 mt-2 text-center">Based on order totals (includes delivery fee)</p>
        </Card>

        <Card class="p-6 border-pink-200">
          <h3 class="text-xl font-bold mb-4">Order Status Distribution</h3>
          <div v-if="statusTotal === 0" class="h-[300px] flex items-center justify-center text-gray-500 text-sm">
            No orders yet — chart will populate after checkout.
          </div>
          <div v-else class="space-y-3">
            <div v-for="s in statusData" :key="s.name" class="flex items-center gap-3">
              <span class="w-24 text-sm text-gray-700">{{ s.name }}</span>
              <div class="flex-1 h-3 rounded-full bg-gray-100 overflow-hidden">
                <div
                  class="h-full rounded-full"
                  :style="{
                    width: `${(s.value / statusTotal) * 100}%`,
                    backgroundColor: s.color,
                  }"
                />
              </div>
              <span class="text-sm font-medium text-gray-800 w-10 text-right">{{ s.value }}</span>
            </div>
          </div>
        </Card>
      </div>

      <Card class="p-6 border-pink-200 mb-8">
        <h3 class="text-xl font-bold mb-4">Sales by Category</h3>
        <div v-if="categoryData.length === 0" class="text-sm text-gray-500 py-8 text-center">
          No category sales yet — totals are computed from order line items.
        </div>
        <div v-else class="space-y-3">
          <div v-for="row in categoryData" :key="row.name" class="flex items-center gap-3">
            <span class="w-28 text-sm text-gray-700 truncate">{{ row.name }}</span>
            <div class="flex-1 h-3 rounded-full bg-gray-100 overflow-hidden">
              <div
                class="h-full rounded-full bg-pink-500"
                :style="{ width: `${(row.sales / maxCategory) * 100}%` }"
              />
            </div>
            <span class="text-sm text-gray-600 w-24 text-right">₱{{ Math.round(row.sales).toLocaleString() }}</span>
          </div>
        </div>
      </Card>

      <Card class="p-6 border-pink-200">
        <h3 class="text-xl font-bold mb-4">Recent Orders</h3>
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="border-b-2 border-pink-200">
                <th class="text-left py-3 px-2">Order ID</th>
                <th class="text-left py-3 px-2">Customer</th>
                <th class="text-left py-3 px-2">Date</th>
                <th class="text-left py-3 px-2">Status</th>
                <th class="text-right py-3 px-2">Total</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="appStore.orders.length === 0">
                <td colspan="5" class="py-8 text-center text-gray-500 text-sm">No orders yet.</td>
              </tr>
              <tr
                v-for="order in appStore.orders.slice(0, 5)"
                :key="order.id"
                class="border-b border-pink-100 hover:bg-pink-50"
              >
                <td class="py-3 px-2 font-medium">{{ order.id }}</td>
                <td class="py-3 px-2">{{ order.customerName }}</td>
                <td class="py-3 px-2">{{ new Date(order.date).toLocaleDateString() }}</td>
                <td class="py-3 px-2">
                  <span
                    class="px-2 py-1 rounded-full text-xs capitalize"
                    :class="{
                      'bg-green-100 text-green-800': order.status === 'delivered',
                      'bg-purple-100 text-purple-800': order.status === 'shipped',
                      'bg-blue-100 text-blue-800': order.status === 'processing',
                      'bg-yellow-100 text-yellow-800': order.status === 'pending',
                      'bg-red-100 text-red-800': order.status === 'cancelled',
                    }"
                  >
                    {{ order.status }}
                  </span>
                </td>
                <td class="py-3 px-2 text-right font-bold text-pink-600">₱{{ order.total.toFixed(2) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  </div>
</template>
