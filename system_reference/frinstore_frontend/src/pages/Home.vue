<script setup lang="ts">
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import { useAppStore } from '@/stores/appStore'
import type { Product } from '@/types/domain'
import { ShoppingCart, Star, Truck, Shield, Clock } from 'lucide-vue-next'
import { toast } from 'vue-sonner'

const appStore = useAppStore()
const featuredProducts = computed(() => appStore.products.slice(0, 4))
const showFeaturedSkeleton = computed(() => appStore.productsLoading && appStore.products.length === 0)

const handleAddToCart = (product: Product) => {
  if (product.stock <= 0) {
    toast.error('This flavor is out of stock.')
    return
  }
  const ok = appStore.addToCart(product)
  if (ok) toast.success(`${product.name} added to cart!`)
  else toast.error('Maximum available quantity is already in your cart.')
}
</script>

<template>
  <div>
    <section class="bg-gradient-to-br from-pink-50 via-pink-100 to-pink-200 py-20">
      <div class="container mx-auto px-4">
        <div class="grid md:grid-cols-2 gap-12 items-center">
          <div>
            <h1 class="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
              Taste the
              <span class="bg-gradient-to-r from-pink-500 to-pink-600 bg-clip-text text-transparent">
                {{ ' ' }}Happiness
              </span>
            </h1>
            <p class="text-xl text-gray-700 mb-8">
              Handcrafted ice cream made with love. Order online and get it delivered to your doorstep!
            </p>
            <div class="flex flex-wrap gap-4">
              <RouterLink to="/products">
                <Button
                  size="lg"
                  class="bg-gradient-to-r from-pink-500 to-pink-600 hover:from-pink-600 hover:to-pink-700 text-lg px-8"
                >
                  Shop Now
                </Button>
              </RouterLink>
              <RouterLink to="/about">
                <Button
                  size="lg"
                  variant="outline"
                  class="border-pink-300 text-pink-600 hover:bg-pink-50 text-lg px-8"
                >
                  Learn More
                </Button>
              </RouterLink>
            </div>
          </div>
          <div class="relative">
            <div class="w-full h-96 bg-white rounded-3xl shadow-2xl overflow-hidden">
              <img
                src="https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=800"
                alt="Ice cream"
                class="w-full h-full object-cover"
              />
            </div>
            <div class="absolute -bottom-6 -left-6 bg-white p-4 rounded-2xl shadow-lg">
              <div class="flex items-center space-x-2">
                <Star class="w-5 h-5 text-yellow-400 fill-yellow-400" />
                <span class="font-bold">4.9/5</span>
                <span class="text-gray-600 text-sm">(2,500+ reviews)</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="py-16 bg-white">
      <div class="container mx-auto px-4">
        <div class="grid md:grid-cols-3 gap-8">
          <Card class="p-6 text-center border-pink-200 hover:shadow-lg transition-shadow">
            <div class="w-16 h-16 bg-pink-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Truck class="w-8 h-8 text-pink-600" />
            </div>
            <h3 class="font-bold text-lg mb-2">Fast Delivery</h3>
            <p class="text-gray-600">Get your ice cream delivered within 30 minutes</p>
          </Card>
          <Card class="p-6 text-center border-pink-200 hover:shadow-lg transition-shadow">
            <div class="w-16 h-16 bg-pink-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Shield class="w-8 h-8 text-pink-600" />
            </div>
            <h3 class="font-bold text-lg mb-2">Quality Guaranteed</h3>
            <p class="text-gray-600">Premium ingredients in every scoop</p>
          </Card>
          <Card class="p-6 text-center border-pink-200 hover:shadow-lg transition-shadow">
            <div class="w-16 h-16 bg-pink-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Clock class="w-8 h-8 text-pink-600" />
            </div>
            <h3 class="font-bold text-lg mb-2">24/7 Support</h3>
            <p class="text-gray-600">We're here to help anytime you need</p>
          </Card>
        </div>
      </div>
    </section>

    <section class="py-16 bg-gradient-to-b from-white to-pink-50">
      <div class="container mx-auto px-4">
        <div class="text-center mb-12">
          <h2 class="text-4xl font-bold text-gray-900 mb-4">Featured Flavors</h2>
          <p class="text-gray-600 text-lg">Try our most popular ice cream flavors</p>
        </div>
        <div v-if="showFeaturedSkeleton" class="text-center py-16 text-gray-600">
          Loading featured flavors…
        </div>
        <div v-else class="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          <Card
            v-for="product in featuredProducts"
            :key="product.id"
            class="overflow-hidden border-pink-200 hover:shadow-xl transition-all duration-300 hover:-translate-y-2"
          >
            <div class="relative h-48 overflow-hidden">
              <img
                :src="product.image"
                :alt="product.name"
                class="w-full h-full object-cover"
              />
              <div class="absolute top-2 right-2 bg-pink-500 text-white px-2 py-1 rounded-full text-sm">
                ₱{{ product.price }}
              </div>
            </div>
            <div class="p-4">
              <h3 class="font-bold text-lg mb-1">{{ product.name }}</h3>
              <p class="text-gray-600 text-sm mb-3 line-clamp-2">{{ product.description }}</p>
              <div class="flex items-center justify-between">
                <span class="text-sm text-pink-600 font-medium">{{ product.category }}</span>
                <Button
                  size="sm"
                  class="bg-gradient-to-r from-pink-500 to-pink-600 hover:from-pink-600 hover:to-pink-700"
                  :disabled="product.stock === 0"
                  @click="handleAddToCart(product)"
                >
                  <ShoppingCart class="w-4 h-4 mr-1" />
                  {{ product.stock === 0 ? 'Out of stock' : 'Add' }}
                </Button>
              </div>
            </div>
          </Card>
        </div>
        <div class="text-center mt-8">
          <RouterLink to="/products">
            <Button size="lg" variant="outline" class="border-pink-300 text-pink-600 hover:bg-pink-50">
              View All Products
            </Button>
          </RouterLink>
        </div>
      </div>
    </section>

    <section class="py-20 bg-gradient-to-r from-pink-500 to-pink-600">
      <div class="container mx-auto px-4 text-center">
        <h2 class="text-4xl font-bold text-white mb-4">Ready to Order?</h2>
        <p class="text-pink-100 text-lg mb-8 max-w-2xl mx-auto">
          Join thousands of happy customers enjoying our delicious ice cream. Order now and get your first delivery free!
        </p>
        <RouterLink to="/products">
          <Button size="lg" class="bg-white text-pink-600 hover:bg-gray-100 text-lg px-8">
            Start Shopping
          </Button>
        </RouterLink>
      </div>
    </section>
  </div>
</template>
