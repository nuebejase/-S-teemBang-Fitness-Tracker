<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import { useAppStore } from '@/stores/appStore'
import type { Order } from '@/types/domain'
import { Search, Package, Clock, CheckCircle, XCircle, Truck, Eye } from 'lucide-vue-next'
import { toast } from 'vue-sonner'

const appStore = useAppStore()

onMounted(() => {
  void appStore.refreshOrders()
})

const searchQuery = ref('')
const selectedStatus = ref('all')
const selectedOrder = ref<Order | null>(null)
const showOrderDetails = ref(false)

const statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']

const filteredOrders = computed(() => {
  let filtered = appStore.orders

  if (searchQuery.value) {
    filtered = filtered.filter(order => 
      order.id.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      order.customerName.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      order.customerEmail.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  }

  if (selectedStatus.value !== 'all') {
    filtered = filtered.filter(order => order.status === selectedStatus.value)
  }

  return filtered.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())
})

const getStatusIcon = (status: Order['status']) => {
  switch (status) {
    case 'pending':
      return Clock
    case 'processing':
      return Package
    case 'shipped':
      return Truck
    case 'delivered':
      return CheckCircle
    case 'cancelled':
      return XCircle
    default:
      return Package
  }
}

const getStatusColor = (status: Order['status']) => {
  switch (status) {
    case 'pending':
      return 'text-yellow-600 bg-yellow-100'
    case 'processing':
      return 'text-blue-600 bg-blue-100'
    case 'shipped':
      return 'text-purple-600 bg-purple-100'
    case 'delivered':
      return 'text-green-600 bg-green-100'
    case 'cancelled':
      return 'text-red-600 bg-red-100'
    default:
      return 'text-gray-600 bg-gray-100'
  }
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const updateOrderStatus = async (orderId: string, newStatus: Order['status']) => {
  try {
    await appStore.updateOrderStatus(orderId, newStatus)
    toast.success(`Order ${orderId} status updated to ${newStatus}`)
  } catch (e) {
    toast.error(e instanceof Error ? e.message : 'Could not update order')
  }
}

const viewOrderDetails = (order: Order) => {
  selectedOrder.value = order
  showOrderDetails.value = true
}

const closeOrderDetails = () => {
  showOrderDetails.value = false
  selectedOrder.value = null
}

const orderStats = computed(() => {
  const stats = {
    total: appStore.orders.length,
    pending: 0,
    processing: 0,
    shipped: 0,
    delivered: 0,
    cancelled: 0,
    revenue: appStore.orders.reduce((sum, order) => sum + order.total, 0),
  }

  for (const order of appStore.orders) {
    if (order.status === 'pending') stats.pending += 1
    else if (order.status === 'processing') stats.processing += 1
    else if (order.status === 'shipped') stats.shipped += 1
    else if (order.status === 'delivered') stats.delivered += 1
    else if (order.status === 'cancelled') stats.cancelled += 1
  }

  return stats
})
</script>

<template>
  <div class="container mx-auto px-4 py-8">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-4xl font-bold text-gray-900 mb-2">Manage Orders</h1>
      <p class="text-gray-600">{{ filteredOrders.length }} orders</p>
    </div>

    <!-- Stats Cards -->
    <div class="grid md:grid-cols-3 lg:grid-cols-6 gap-4 mb-8">
      <Card class="p-4 text-center border-pink-200">
        <div class="text-2xl font-bold text-gray-900">{{ orderStats.total }}</div>
        <div class="text-sm text-gray-600">Total</div>
      </Card>
      <Card class="p-4 text-center border-yellow-200">
        <div class="text-2xl font-bold text-yellow-600">{{ orderStats.pending }}</div>
        <div class="text-sm text-gray-600">Pending</div>
      </Card>
      <Card class="p-4 text-center border-blue-200">
        <div class="text-2xl font-bold text-blue-600">{{ orderStats.processing }}</div>
        <div class="text-sm text-gray-600">Processing</div>
      </Card>
      <Card class="p-4 text-center border-purple-200">
        <div class="text-2xl font-bold text-purple-600">{{ orderStats.shipped }}</div>
        <div class="text-sm text-gray-600">Shipped</div>
      </Card>
      <Card class="p-4 text-center border-green-200">
        <div class="text-2xl font-bold text-green-600">{{ orderStats.delivered }}</div>
        <div class="text-sm text-gray-600">Delivered</div>
      </Card>
      <Card class="p-4 text-center border-red-200">
        <div class="text-2xl font-bold text-red-600">{{ orderStats.cancelled }}</div>
        <div class="text-sm text-gray-600">Cancelled</div>
      </Card>
    </div>

    <!-- Filters -->
    <div class="bg-white rounded-lg shadow-sm border p-6 mb-8">
      <div class="grid md:grid-cols-2 gap-4">
        <!-- Search -->
        <div class="relative">
          <Search class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search orders by ID, customer name, or email..."
            class="w-full pl-10 pr-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500"
          />
        </div>

        <!-- Status Filter -->
        <select
          v-model="selectedStatus"
          class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500"
        >
          <option value="all">All Statuses</option>
          <option v-for="status in statuses" :key="status" :value="status">
            {{ status.charAt(0).toUpperCase() + status.slice(1) }}
          </option>
        </select>
      </div>
    </div>

    <!-- Orders List -->
    <div class="space-y-4">
      <Card v-for="order in filteredOrders" :key="order.id" class="overflow-hidden">
        <div class="p-6">
          <!-- Order Header -->
          <div class="flex items-center justify-between mb-4">
            <div class="flex items-center space-x-4">
              <div>
                <div class="flex items-center space-x-3 mb-1">
                  <h3 class="text-lg font-semibold">Order #{{ order.id }}</h3>
                  <span :class="`px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(order.status)}`">
                    <component :is="getStatusIcon(order.status)" class="w-3 h-3 inline mr-1" />
                    {{ order.status.charAt(0).toUpperCase() + order.status.slice(1) }}
                  </span>
                </div>
                <p class="text-gray-600 text-sm">{{ formatDate(order.date) }}</p>
              </div>
            </div>
            <div class="text-right">
              <p class="text-2xl font-bold">₱{{ order.total }}</p>
              <p class="text-sm text-gray-600">{{ order.items.length }} items</p>
            </div>
          </div>

          <!-- Customer Info -->
          <div class="bg-gray-50 rounded-lg p-4 mb-4">
            <div class="grid md:grid-cols-3 gap-4 text-sm">
              <div>
                <p class="font-medium text-gray-700">Customer</p>
                <p class="text-gray-600">{{ order.customerName }}</p>
                <p class="text-gray-600">{{ order.customerEmail }}</p>
                <p class="text-gray-600">{{ order.customerPhone }}</p>
              </div>
              <div>
                <p class="font-medium text-gray-700">Payment</p>
                <p class="text-gray-600">{{ order.paymentMethod }}</p>
              </div>
              <div>
                <p class="font-medium text-gray-700">Address</p>
                <p class="text-gray-600">{{ order.address }}</p>
              </div>
            </div>
          </div>

          <!-- Order Actions -->
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-2">
              <span class="text-sm text-gray-600">Update Status:</span>
              <select
                :value="order.status"
                class="px-3 py-1 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-pink-500"
                @change="
                  updateOrderStatus(
                    order.id,
                    ($event.target as HTMLSelectElement).value as Order['status'],
                  )
                "
              >
                <option value="pending">Pending</option>
                <option value="processing">Processing</option>
                <option value="shipped">Shipped</option>
                <option value="delivered">Delivered</option>
                <option value="cancelled">Cancelled</option>
              </select>
            </div>
            <Button @click="viewOrderDetails(order)" variant="outline" size="sm">
              <Eye class="w-4 h-4 mr-2" />
              View Details
            </Button>
          </div>
        </div>
      </Card>
    </div>

    <!-- Empty State -->
    <div v-if="filteredOrders.length === 0" class="text-center py-12">
      <div class="text-gray-400 mb-4">
        <Package class="w-16 h-16 mx-auto" />
      </div>
      <h3 class="text-xl font-semibold text-gray-700 mb-2">No orders found</h3>
      <p class="text-gray-600">Try adjusting your filters</p>
    </div>

    <!-- Order Details Modal -->
    <div v-if="showOrderDetails && selectedOrder" class="fixed inset-0 z-50 overflow-hidden">
      <div class="absolute inset-0 bg-black bg-opacity-50" @click="closeOrderDetails"></div>
      <div class="absolute right-0 top-0 h-full w-full max-w-2xl bg-white shadow-xl overflow-y-auto">
        <div class="p-6">
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-2xl font-bold">Order Details</h2>
            <Button @click="closeOrderDetails" variant="ghost" size="sm">
              <XCircle class="w-5 h-5" />
            </Button>
          </div>

          <div class="space-y-6">
            <!-- Order Info -->
            <div class="bg-gray-50 rounded-lg p-4">
              <h3 class="font-semibold mb-3">Order Information</h3>
              <div class="grid md:grid-cols-2 gap-4 text-sm">
                <div>
                  <p class="font-medium text-gray-700">Order ID</p>
                  <p class="text-gray-600">{{ selectedOrder.id }}</p>
                </div>
                <div>
                  <p class="font-medium text-gray-700">Date</p>
                  <p class="text-gray-600">{{ formatDate(selectedOrder.date) }}</p>
                </div>
                <div>
                  <p class="font-medium text-gray-700">Status</p>
                  <span :class="`px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(selectedOrder.status)}`">
                    {{ selectedOrder.status.charAt(0).toUpperCase() + selectedOrder.status.slice(1) }}
                  </span>
                </div>
                <div>
                  <p class="font-medium text-gray-700">Total</p>
                  <p class="text-gray-600 font-semibold">₱{{ selectedOrder.total }}</p>
                </div>
              </div>
            </div>

            <!-- Customer Info -->
            <div class="bg-gray-50 rounded-lg p-4">
              <h3 class="font-semibold mb-3">Customer Information</h3>
              <div class="grid md:grid-cols-2 gap-4 text-sm">
                <div>
                  <p class="font-medium text-gray-700">Name</p>
                  <p class="text-gray-600">{{ selectedOrder.customerName }}</p>
                </div>
                <div>
                  <p class="font-medium text-gray-700">Email</p>
                  <p class="text-gray-600">{{ selectedOrder.customerEmail }}</p>
                </div>
                <div>
                  <p class="font-medium text-gray-700">Phone</p>
                  <p class="text-gray-600">{{ selectedOrder.customerPhone }}</p>
                </div>
                <div class="md:col-span-2">
                  <p class="font-medium text-gray-700">Address</p>
                  <p class="text-gray-600">{{ selectedOrder.address }}</p>
                </div>
              </div>
            </div>

            <!-- Order Items -->
            <div>
              <h3 class="font-semibold mb-3">Order Items</h3>
              <div class="space-y-3">
                <div v-for="item in selectedOrder.items" :key="item.id" class="flex items-center space-x-4 bg-gray-50 rounded-lg p-3">
                  <img
                    :src="item.image"
                    :alt="item.name"
                    class="w-16 h-16 object-cover rounded"
                  />
                  <div class="flex-1">
                    <h4 class="font-medium">{{ item.name }}</h4>
                    <p class="text-sm text-gray-600">{{ item.flavor }} • {{ item.category }}</p>
                  </div>
                  <div class="text-right">
                    <p class="font-medium">₱{{ item.price * item.quantity }}</p>
                    <p class="text-sm text-gray-600">₱{{ item.price }} x {{ item.quantity }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
