<script setup lang="ts">
import { computed, ref } from 'vue'
import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import { useAppStore } from '@/stores/appStore'
import type { Product } from '@/types/domain'
import { ShoppingCart, Search } from 'lucide-vue-next'
import { toast } from 'vue-sonner'

const appStore = useAppStore()

const searchQuery = ref('')
const categoryFilter = ref('all')
const sortBy = ref<'name' | 'price-low' | 'price-high'>('name')

const categories = computed(() => {
  const unique = new Set(appStore.products.map((p) => p.category))
  return ['all', ...unique] as string[]
})

const filteredProducts = computed(() => {
  const q = searchQuery.value.toLowerCase()
  return appStore.products
    .filter((product) => {
      const matchesSearch =
        !q ||
        product.name.toLowerCase().includes(q) ||
        product.flavor.toLowerCase().includes(q) ||
        product.description.toLowerCase().includes(q)
      const matchesCategory =
        categoryFilter.value === 'all' || product.category === categoryFilter.value
      return matchesSearch && matchesCategory
    })
    .sort((a, b) => {
      if (sortBy.value === 'price-low') return a.price - b.price
      if (sortBy.value === 'price-high') return b.price - a.price
      return a.name.localeCompare(b.name)
    })
})

const handleAddToCart = (product: Product) => {
  if (product.stock <= 0) {
    toast.error('This flavor is out of stock.')
    return
  }
  const ok = appStore.addToCart(product)
  if (ok) toast.success(`${product.name} added to cart!`)
  else toast.error('Maximum available quantity is already in your cart.')
}

const formatCategoryLabel = (c: string) =>
  c === 'all' ? 'All categories' : c.charAt(0).toUpperCase() + c.slice(1)
</script>

<template>
  <div class="min-h-screen bg-gradient-to-b from-pink-50 to-white">
    <div class="container mx-auto px-4 py-8">
      <div class="mb-8">
        <h1 class="text-4xl font-bold text-gray-900 mb-2">Our Ice Cream Collection</h1>
        <p class="text-gray-600">Discover all our delicious flavors</p>
        <p v-if="appStore.productsLoading" class="text-sm text-pink-600 mt-2">Loading catalog…</p>
      </div>

      <div class="bg-white p-6 rounded-xl shadow-sm border border-pink-200 mb-8">
        <div class="grid md:grid-cols-3 gap-4">
          <div class="relative">
            <Search
              class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 w-5 h-5 pointer-events-none"
            />
            <input
              v-model="searchQuery"
              type="search"
              placeholder="Search flavors..."
              class="w-full pl-10 pr-4 py-2 rounded-md border border-pink-200 bg-background text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
            />
          </div>
          <select
            v-model="categoryFilter"
            class="w-full px-3 py-2 rounded-md border border-pink-200 bg-background text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          >
            <option v-for="category in categories" :key="category" :value="category">
              {{ formatCategoryLabel(category) }}
            </option>
          </select>
          <select
            v-model="sortBy"
            class="w-full px-3 py-2 rounded-md border border-pink-200 bg-background text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          >
            <option value="name">Name (A-Z)</option>
            <option value="price-low">Price (Low to High)</option>
            <option value="price-high">Price (High to Low)</option>
          </select>
        </div>
      </div>

      <div v-if="filteredProducts.length > 0" class="grid md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        <Card
          v-for="product in filteredProducts"
          :key="product.id"
          class="overflow-hidden border-pink-200 hover:shadow-xl transition-all duration-300 hover:-translate-y-2"
        >
          <div class="relative h-56 overflow-hidden">
            <img
              :src="product.image"
              :alt="product.name"
              class="w-full h-full object-cover"
            />
            <div class="absolute top-3 right-3 bg-pink-500 text-white px-3 py-1 rounded-full font-bold">
              ₱{{ product.price }}
            </div>
            <div
              v-if="product.stock < 10"
              class="absolute top-3 left-3 bg-red-500 text-white px-2 py-1 rounded-full text-xs"
            >
              Low Stock
            </div>
          </div>
          <div class="p-5">
            <div class="mb-2">
              <h3 class="font-bold text-lg mb-1">{{ product.name }}</h3>
              <span class="text-xs bg-pink-100 text-pink-600 px-2 py-1 rounded-full">
                {{ product.category }}
              </span>
            </div>
            <p class="text-gray-600 text-sm mb-3 line-clamp-2">{{ product.description }}</p>
            <div class="flex items-center justify-between mb-3">
              <span class="text-sm text-gray-500">Flavor: {{ product.flavor }}</span>
              <span class="text-sm text-gray-500">Stock: {{ product.stock }}</span>
            </div>
            <Button
              class="w-full bg-gradient-to-r from-pink-500 to-pink-600 hover:from-pink-600 hover:to-pink-700"
              :disabled="product.stock === 0"
              @click="handleAddToCart(product)"
            >
              <ShoppingCart class="w-4 h-4 mr-2" />
              {{ product.stock === 0 ? 'Out of Stock' : 'Add to Cart' }}
            </Button>
          </div>
        </Card>
      </div>

      <div v-else class="text-center py-20">
        <div class="text-6xl mb-4" aria-hidden="true">🍦</div>
        <h3 class="text-2xl font-bold text-gray-900 mb-2">No products found</h3>
        <p class="text-gray-600">Try adjusting your search or filters</p>
      </div>
    </div>
  </div>
</template>
