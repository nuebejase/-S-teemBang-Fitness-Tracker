<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import { useAppStore } from '@/stores/appStore'
import { CreditCard, Smartphone, CheckCircle2 } from 'lucide-vue-next'
import { toast } from 'vue-sonner'

const router = useRouter()
const appStore = useAppStore()

const showConfirmation = ref(false)
const orderId = ref('')
/** True while createOrder is in flight so cart-empty watch does not redirect before the success modal opens. */
const placingOrder = ref(false)

const formData = ref({
  name: appStore.user?.name ?? '',
  email: appStore.user?.email ?? '',
  phone: '',
  address: '',
  paymentMethod: 'gcash',
})

watch(
  () => appStore.user,
  (u) => {
    if (u) {
      formData.value.name = u.name
      formData.value.email = u.email
    }
  },
  { immediate: true },
)

const cart = computed(() => appStore.cart)

const subtotal = computed(() =>
  cart.value.reduce((sum, item) => sum + item.price * item.quantity, 0),
)
const deliveryFee = 50
const total = computed(() => subtotal.value + deliveryFee)

watch(
  cart,
  (c) => {
    if (c.length === 0 && !showConfirmation.value && !placingOrder.value) {
      router.replace('/cart')
    }
  },
  { deep: true, immediate: true },
)

const handleSubmit = async () => {
  if (!formData.value.name || !formData.value.email || !formData.value.phone || !formData.value.address) {
    toast.error('Please fill in all required fields')
    return
  }

  placingOrder.value = true
  try {
    const order = await appStore.createOrder({
      customerName: formData.value.name,
      customerEmail: formData.value.email,
      customerPhone: formData.value.phone,
      address: formData.value.address,
      paymentMethod: formData.value.paymentMethod,
      status: 'pending',
    })

    orderId.value = order.id
    showConfirmation.value = true
    toast.success('Order placed!')
  } catch (err) {
    const msg = err instanceof Error ? err.message : 'Could not place order'
    toast.error(msg)
  } finally {
    placingOrder.value = false
  }
}

const handleConfirmationClose = () => {
  showConfirmation.value = false
  router.push('/orders')
}
</script>

<template>
  <div v-if="cart.length > 0" class="min-h-screen bg-gradient-to-b from-pink-50 to-white py-8">
    <div class="container mx-auto px-4">
      <h1 class="text-4xl font-bold text-gray-900 mb-8">Checkout</h1>

      <form @submit.prevent="handleSubmit">
        <div class="grid lg:grid-cols-3 gap-8">
          <div class="lg:col-span-2 space-y-6">
            <Card class="p-6 border-pink-200">
              <h2 class="text-2xl font-bold mb-4">Contact Information</h2>
              <div class="space-y-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1" for="co-name">Full Name *</label>
                  <input
                    id="co-name"
                    v-model="formData.name"
                    name="name"
                    required
                    autocomplete="name"
                    placeholder="Juan Dela Cruz"
                    class="w-full px-3 py-2 rounded-md border border-pink-200 bg-background text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1" for="co-email">Email *</label>
                  <input
                    id="co-email"
                    v-model="formData.email"
                    name="email"
                    type="email"
                    required
                    autocomplete="email"
                    placeholder="juan@example.com"
                    class="w-full px-3 py-2 rounded-md border border-pink-200 bg-background text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1" for="co-phone">Phone Number *</label>
                  <input
                    id="co-phone"
                    v-model="formData.phone"
                    name="phone"
                    type="tel"
                    required
                    autocomplete="tel"
                    placeholder="09XX XXX XXXX"
                    class="w-full px-3 py-2 rounded-md border border-pink-200 bg-background text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                  />
                </div>
              </div>
            </Card>

            <Card class="p-6 border-pink-200">
              <h2 class="text-2xl font-bold mb-4">Delivery Address</h2>
              <label class="block text-sm font-medium text-gray-700 mb-1" for="co-address">Complete Address *</label>
              <textarea
                id="co-address"
                v-model="formData.address"
                name="address"
                required
                rows="4"
                placeholder="House No., Street, Barangay, City, Province"
                class="w-full px-3 py-2 rounded-md border border-pink-200 bg-background text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
              />
            </Card>

            <Card class="p-6 border-pink-200">
              <h2 class="text-2xl font-bold mb-4">Payment Method</h2>
              <div class="space-y-3">
                <label
                  class="flex items-center space-x-3 p-4 border-2 border-pink-200 rounded-lg hover:bg-pink-50 cursor-pointer"
                >
                  <input v-model="formData.paymentMethod" type="radio" value="gcash" class="text-pink-600" />
                  <Smartphone class="w-5 h-5 text-blue-600 shrink-0" />
                  <span>GCash</span>
                </label>
                <label
                  class="flex items-center space-x-3 p-4 border-2 border-pink-200 rounded-lg hover:bg-pink-50 cursor-pointer"
                >
                  <input v-model="formData.paymentMethod" type="radio" value="card" class="text-pink-600" />
                  <CreditCard class="w-5 h-5 text-pink-600 shrink-0" />
                  <span>Credit/Debit Card</span>
                </label>
                <label
                  class="flex items-center space-x-3 p-4 border-2 border-pink-200 rounded-lg hover:bg-pink-50 cursor-pointer"
                >
                  <input v-model="formData.paymentMethod" type="radio" value="cod" class="text-pink-600" />
                  <span class="text-lg" aria-hidden="true">💵</span>
                  <span>Cash on Delivery</span>
                </label>
              </div>
            </Card>
          </div>

          <div class="lg:col-span-1">
            <Card class="p-6 border-pink-200 lg:sticky lg:top-24">
              <h2 class="text-2xl font-bold mb-4">Order Summary</h2>
              <div class="space-y-3 mb-4">
                <div
                  v-for="item in cart"
                  :key="item.id"
                  class="flex justify-between text-sm gap-2"
                >
                  <span class="text-gray-700 truncate">{{ item.name }} x {{ item.quantity }}</span>
                  <span class="font-medium shrink-0">₱{{ (item.price * item.quantity).toFixed(2) }}</span>
                </div>
              </div>
              <div class="border-t-2 border-pink-200 pt-3 space-y-2 mb-4">
                <div class="flex justify-between text-gray-700">
                  <span>Subtotal</span>
                  <span>₱{{ subtotal.toFixed(2) }}</span>
                </div>
                <div class="flex justify-between text-gray-700">
                  <span>Delivery Fee</span>
                  <span>₱{{ deliveryFee.toFixed(2) }}</span>
                </div>
                <div class="flex justify-between text-xl font-bold pt-2">
                  <span>Total</span>
                  <span class="text-pink-600">₱{{ total.toFixed(2) }}</span>
                </div>
              </div>
              <Button
                type="submit"
                class="w-full bg-gradient-to-r from-pink-500 to-pink-600 hover:from-pink-600 hover:to-pink-700 h-12 text-lg"
              >
                Place Order
              </Button>
              <p class="text-xs text-gray-500 text-center mt-3 space-y-1">
                <span class="block">By placing this order, you agree to our terms and conditions.</span>
                <span class="block">Payment method is recorded for fulfillment only — no live gateway in this demo.</span>
              </p>
            </Card>
          </div>
        </div>
      </form>
    </div>
  </div>

  <Teleport to="body">
    <div
      v-if="showConfirmation"
      class="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/50"
      role="dialog"
      aria-modal="true"
      aria-labelledby="confirm-title"
    >
      <div class="bg-white rounded-lg shadow-lg max-w-md w-full p-6 space-y-4">
        <div class="flex justify-center mb-2">
          <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center">
            <CheckCircle2 class="w-10 h-10 text-green-600" />
          </div>
        </div>
        <h2 id="confirm-title" class="text-center text-2xl font-bold">Order Confirmed!</h2>
        <p class="text-center text-gray-600 text-sm">
          Your order has been successfully placed.
        </p>
        <div class="bg-pink-50 p-4 rounded-lg text-center">
          <p class="text-sm text-gray-600 mb-1">Order Number</p>
          <p class="text-xl font-bold text-pink-600">{{ orderId }}</p>
        </div>
        <p class="text-sm text-gray-600 text-center">
          We've sent a confirmation email to <strong>{{ formData.email }}</strong>
        </p>
        <Button
          class="w-full bg-gradient-to-r from-pink-500 to-pink-600 hover:from-pink-600 hover:to-pink-700"
          type="button"
          @click="handleConfirmationClose"
        >
          Track My Order
        </Button>
      </div>
    </div>
  </Teleport>
</template>
