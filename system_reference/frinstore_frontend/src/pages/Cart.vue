<script setup lang="ts">
import { computed } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import { useAppStore } from '@/stores/appStore'
import { Minus, Plus, Trash2, ShoppingBag } from 'lucide-vue-next'

const appStore = useAppStore()
const router = useRouter()

const cart = computed(() => appStore.cart)

const subtotal = computed(() =>
  cart.value.reduce((sum, item) => sum + item.price * item.quantity, 0),
)
const deliveryFee = computed(() => (subtotal.value > 0 ? 50 : 0))
const total = computed(() => subtotal.value + deliveryFee.value)

const handleCheckout = () => {
  if (cart.value.length > 0) {
    router.push('/checkout')
  }
}
</script>

<template>
  <div v-if="cart.length === 0" class="min-h-screen bg-gradient-to-b from-pink-50 to-white flex items-center justify-center">
    <div class="text-center py-20 px-4">
      <div class="text-8xl mb-6" aria-hidden="true">🛒</div>
      <h2 class="text-3xl font-bold text-gray-900 mb-4">Your cart is empty</h2>
      <p class="text-gray-600 mb-8">Add some delicious ice cream to get started!</p>
      <RouterLink to="/products">
        <Button size="lg" class="bg-gradient-to-r from-pink-500 to-pink-600 hover:from-pink-600 hover:to-pink-700">
          <ShoppingBag class="w-5 h-5 mr-2" />
          Browse Products
        </Button>
      </RouterLink>
    </div>
  </div>

  <div v-else class="min-h-screen bg-gradient-to-b from-pink-50 to-white py-8">
    <div class="container mx-auto px-4">
      <h1 class="text-4xl font-bold text-gray-900 mb-8">Shopping Cart</h1>

      <div class="grid lg:grid-cols-3 gap-8">
        <div class="lg:col-span-2 space-y-4">
          <Card v-for="item in cart" :key="item.id" class="p-4 border-pink-200">
            <div class="flex gap-4">
              <div class="w-24 h-24 rounded-lg overflow-hidden shrink-0">
                <img :src="item.image" :alt="item.name" class="w-full h-full object-cover" />
              </div>
              <div class="flex-1 min-w-0">
                <div class="flex justify-between items-start mb-2 gap-2">
                  <div>
                    <h3 class="font-bold text-lg">{{ item.name }}</h3>
                    <p class="text-sm text-gray-600">{{ item.flavor }}</p>
                  </div>
                  <Button
                    variant="ghost"
                    size="icon"
                    class="text-red-500 hover:text-red-700 hover:bg-red-50 shrink-0"
                    type="button"
                    aria-label="Remove item"
                    @click="appStore.removeFromCart(item.id)"
                  >
                    <Trash2 class="w-5 h-5" />
                  </Button>
                </div>
                <div class="flex flex-wrap items-center justify-between gap-2">
                  <div class="flex items-center gap-3">
                    <Button
                      variant="outline"
                      size="icon"
                      class="h-8 w-8 border-pink-300"
                      type="button"
                      aria-label="Decrease quantity"
                      @click="appStore.updateCartQuantity(item.id, item.quantity - 1)"
                    >
                      <Minus class="w-4 h-4" />
                    </Button>
                    <input
                      :value="item.quantity"
                      type="number"
                      min="1"
                      :max="item.stock"
                      class="w-16 h-8 text-center border border-pink-200 rounded-md text-sm bg-background"
                      @change="
                        appStore.updateCartQuantity(
                          item.id,
                          Number(($event.target as HTMLInputElement).value) || 1,
                        )
                      "
                    />
                    <Button
                      variant="outline"
                      size="icon"
                      class="h-8 w-8 border-pink-300"
                      type="button"
                      aria-label="Increase quantity"
                      :disabled="item.quantity >= item.stock"
                      @click="appStore.updateCartQuantity(item.id, item.quantity + 1)"
                    >
                      <Plus class="w-4 h-4" />
                    </Button>
                  </div>
                  <div class="text-right">
                    <p class="font-bold text-lg text-pink-600">
                      ₱{{ (item.price * item.quantity).toFixed(2) }}
                    </p>
                    <p class="text-sm text-gray-500">₱{{ item.price }} each</p>
                  </div>
                </div>
              </div>
            </div>
          </Card>
        </div>

        <div class="lg:col-span-1">
          <Card class="p-6 border-pink-200 lg:sticky lg:top-24">
            <h2 class="text-2xl font-bold mb-6">Order Summary</h2>
            <div class="space-y-3 mb-6">
              <div class="flex justify-between text-gray-700">
                <span>Subtotal ({{ cart.length }} items)</span>
                <span>₱{{ subtotal.toFixed(2) }}</span>
              </div>
              <div class="flex justify-between text-gray-700">
                <span>Delivery Fee</span>
                <span>₱{{ deliveryFee.toFixed(2) }}</span>
              </div>
              <div class="border-t-2 border-pink-200 pt-3">
                <div class="flex justify-between text-xl font-bold">
                  <span>Total</span>
                  <span class="text-pink-600">₱{{ total.toFixed(2) }}</span>
                </div>
              </div>
            </div>
            <Button
              class="w-full bg-gradient-to-r from-pink-500 to-pink-600 hover:from-pink-600 hover:to-pink-700 h-12 text-lg"
              type="button"
              @click="handleCheckout"
            >
              Proceed to Checkout
            </Button>
            <RouterLink to="/products">
              <Button variant="outline" class="w-full mt-3 border-pink-300 text-pink-600 hover:bg-pink-50">
                Continue Shopping
              </Button>
            </RouterLink>
          </Card>
        </div>
      </div>
    </div>
  </div>
</template>
